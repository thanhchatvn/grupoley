odoo.define('pos_cupones_descuentos.pos', function (require) {
    'use strict';

    const models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    const session = require('web.session');
    const concurrency = require('web.concurrency');
    const { Gui } = require('point_of_sale.Gui');

    const dp = new concurrency.DropPrevious();

    class CouponCode {
        constructor(code, coupon_id, program_id) {
            this.code = code;
            this.coupon_id = coupon_id;
            this.program_id = program_id;
        }
    }

    class Reward {
        static createKey(program_id, coupon_id) {
            return coupon_id ? `${program_id}-${coupon_id}` : `${program_id}`;
        }
        constructor({
            product,
            unit_price,
            quantity,
            program,
            tax_ids,
            coupon_id = undefined,
            awarded = true,
            reason = undefined,
        }) {
            this.product = product;
            this.unit_price = unit_price;
            this.quantity = quantity;
            this.program = program;
            this.tax_ids = tax_ids;
            this.coupon_id = coupon_id;
            this._discountAmount = Math.abs(unit_price * quantity);
            this.status = {
                awarded,
                reason,
            };
            this._key = Reward.createKey(program.id, coupon_id);
        }

        get rewardedProductId() {
            return (
                this.program.reward_type == 'product' &&
                this.program.reward_product_id &&
                this.program.reward_product_id[0]
            );
        }
        get discountAmount() {
            return this._discountAmount;
        }
        get key() {
            return this._key;
        }
    }

    class RewardsContainer {

        constructor() {
            this._rewards = {};
        }
        clear() {
            this._rewards = {};
        }
        add(rewards) {
            for (const reward of rewards) {
                if (reward.key in this._rewards) {
                    this._rewards[reward.key].push(reward);
                } else {
                    this._rewards[reward.key] = [reward];
                }
            }
        }
        getUnawarded() {
            return this._getFlattenRewards().filter((reward) => !reward.status.awarded);
        }
        getAwarded() {
            return this._getFlattenRewards().filter((reward) => reward.status.awarded);
        }
        _getFlattenRewards() {
            return Object.values(this._rewards).reduce((flatArr, arr) => [...flatArr, ...arr], []);
        }
    }

    function computeFreeQuantity(numberItems, n, m) {
        let factor = Math.trunc(numberItems / (n + m));
        let free = factor * m;
        let charged = numberItems - free;
        let x = (factor + 1) * n;
        let y = x + (factor + 1) * m;
        let adjustment = x <= charged && charged < y ? charged - x : 0;
        return free + adjustment;
    }

    models.load_fields('product.product', 'desc_pos');

    var existing_models = models.PosModel.prototype.models;
    var product_index = _.findIndex(existing_models, function (model) {
        return model.model === 'product.product';
    });
    var product_model = existing_models[product_index];
    models.load_models([
        {
            model: 'coupon.program',
            fields: [],
            domain: function (self) {
                return [['id', 'in', self.config.program_ids]];
            },
            loaded: function (self, programs) {
                self.programs = programs;
                self.coupon_programs_by_id = {};
                self.coupon_programs = [];
                self.promo_programs = [];
                for (let program of self.programs) {
                    self.coupon_programs_by_id[program.id] = program;
                    if (program.program_type === 'coupon_program') {
                        self.coupon_programs.push(program);
                    } else {
                        self.promo_programs.push(program);
                    }
                    program.valid_product_ids = new Set(program.valid_product_ids);
                    program.valid_partner_ids = new Set(program.valid_partner_ids);
                    program.discount_specific_product_ids = new Set(program.discount_specific_product_ids);
                }
            },
        },
        {
            model: product_model.model,
            fields: product_model.fields,
            order: product_model.order,
            domain: function (self) {
//                Object.filter = (obj, predicate) =>
//                    Object.keys(obj)
//                          .filter( key => predicate(obj[key]) )
//                          .reduce( (res, key) => (res[key] = obj[key], res), {} );
//                let producto_dscto = Object.filter(this.pos.db.product_by_id, e => e.desc_pos == true);

                const discountLineProductIds = self.programs.map((program) => program.discount_line_product_id[0]);

                const rewardProductIds = self.programs.map((program) => program.reward_product_id[0]);
                return [['id', 'in', discountLineProductIds.concat(rewardProductIds)]];
            },
            context: product_model.context,
            loaded: product_model.loaded,
        },
    ]);

    var _posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function () {
            _posmodel_super.initialize.apply(this, arguments);
            this.ready.then(() => {
                if (this.get('selectedOrder')) {
                    this.get('selectedOrder').trigger('update-rewards');
                }
            });
        },
    });

    var _order_super = models.Order.prototype;
    models.Order = models.Order.extend({

        initialize: function () {
            let res = _order_super.initialize.apply(this, arguments);
            res.on(
                'update-rewards',
                () => {
                    if (!this.pos.config.use_coupon_programs) return;
                    dp.add(this._getNewRewardLines()).then(([newRewardLines, rewardsContainer]) => {
                        this.orderlines.remove(this._getRewardLines());
                        this.orderlines.add(newRewardLines);
                        this.rewardsContainer = rewardsContainer;
                        this.trigger('rewards-updated');
                    }).catch((err) => {
                        console.log(err)
                    });
                },
                res
            );
            res.on('reset-coupons', res.resetCoupons, res);
            res._initializePrograms();
            return res;
        },
        init_from_JSON: function (json) {
            _order_super.init_from_JSON.apply(this, arguments);
            this.bookedCouponCodes = json.bookedCouponCodes;
            this.activePromoProgramIds = json.activePromoProgramIds;
        },
        export_as_JSON: function () {
            let json = _order_super.export_as_JSON.apply(this, arguments);
            return Object.assign(json, {
                bookedCouponCodes: this.bookedCouponCodes,
                activePromoProgramIds: this.activePromoProgramIds,
            });
        },
        add_product: function(product, options){
            if(this._printed){
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var line = new exports.Orderline({}, {pos: this.pos, order: this, product: product});
            this.fix_tax_included_price(line);

            this.set_orderline_options(line, options);

            var to_merge_orderline;
            for (var i = 0; i < this.orderlines.length; i++) {
                if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                    to_merge_orderline = this.orderlines.at(i);
                }
            }
            if (to_merge_orderline){
                to_merge_orderline.merge(line);
                this.select_orderline(to_merge_orderline);
            } else {
                this.orderlines.add(line);
                this.select_orderline(this.get_last_orderline());
            }

            if (options.draftPackLotLines) {
                this.selected_orderline.setPackLotLines(options.draftPackLotLines);
            }
            if (this.pos.config.iface_customer_facing_display) {
                this.pos.send_current_order_to_customer_facing_display();
            }
        },
        set_orderline_options: function(orderline, options) {
            if(options.quantity !== undefined){
                orderline.set_quantity(options.quantity);
            }

            if(options.price !== undefined){
                orderline.set_unit_price(options.price);
                this.fix_tax_included_price(orderline);
            }

            if (options.price_extra !== undefined){
                orderline.price_extra = options.price_extra;
                orderline.set_unit_price(orderline.product.get_price(this.pricelist, orderline.get_quantity(), options.price_extra));
                this.fix_tax_included_price(orderline);
            }

            if(options.lst_price !== undefined){
                orderline.set_lst_price(options.lst_price);
            }

            if(options.discount !== undefined){
                orderline.set_discount(options.discount);
            }

            if (options.description !== undefined){
                orderline.description += options.description;
            }

            if(options.extras !== undefined){
                for (var prop in options.extras) {
                    orderline[prop] = options.extras[prop];
                }
            }
            if (options.is_tip) {
                this.is_tipped = true;
                this.tip_amount = options.price;
            }
            if (options && options.is_program_reward) {
                orderline.is_program_reward = true;
                orderline.tax_ids = options.tax_ids;
                orderline.program_id = options.program_id;
                orderline.coupon_id = options.coupon_id;
            }
        },
        get_orderlines: function () {
            return [...this._getRegularOrderlines(), ...this._getRewardLines()];
        },
        _getRegularOrderlines: function () {
            const orderlines = _order_super.get_orderlines.apply(this, arguments);
            return orderlines.filter((line) => !line.is_program_reward);
        },
        _getRewardLines: function () {
            const orderlines = _order_super.get_orderlines.apply(this, arguments);
            return orderlines.filter((line) => line.is_program_reward);
        },
        wait_for_push_order: function () {
            return (
                (this.programIdsToGenerateCoupons && this.programIdsToGenerateCoupons.length) ||
                this.get_orderlines().filter((line) => line.is_program_reward).length ||
                _order_super.wait_for_push_order.apply(this, arguments)
            );
        },
        export_for_printing: function () {
            let result = _order_super.export_for_printing.apply(this, arguments);
            result.generated_coupons = this.generated_coupons;
            return result;
        },
        add_product: function (product, options) {
            _order_super.add_product.apply(this, [product, options]);
            this.trigger('update-rewards');
        },
        get_last_orderline: function () {
            const regularLines = _order_super.get_orderlines
                .apply(this, arguments)
                .filter((line) => !line.is_program_reward);
            return regularLines[regularLines.length - 1];
        },

        _initializePrograms: async function () {
            if (!this.bookedCouponCodes) {
                this.bookedCouponCodes = {};
            }
            if (!this.activePromoProgramIds) {
                this.activePromoProgramIds = this._getAutomaticPromoProgramIds();
            }
        },
        resetPrograms: function () {
            let deactivatedCount = 0;
            if (this.bookedCouponCodes) {
                const couponIds = Object.values(this.bookedCouponCodes).map((couponCode) => couponCode.coupon_id);
                if (couponIds.length > 0) {
                    this.trigger('reset-coupons', couponIds);
                }
                this.bookedCouponCodes = {};
                deactivatedCount += couponIds.length;
            }
            if (this.activePromoProgramIds) {
                const codeNeededPromoProgramIds = this.activePromoProgramIds.filter((program_id) => {
                    return this.pos.coupon_programs_by_id[program_id].promo_code_usage === 'code_needed';
                });
                this.activePromoProgramIds = this._getAutomaticPromoProgramIds();
                deactivatedCount += codeNeededPromoProgramIds.length;
            }
            if (deactivatedCount > 0) Gui.showNotification('Active coupons and promo codes were deactivated.');
            this.trigger('update-rewards');
        },

        activateCode: async function (code) {
            const promoProgram = this.pos.promo_programs.find(
                (program) => program.promo_barcode == code || program.promo_code == code
            );
            if (promoProgram && this.activePromoProgramIds.includes(promoProgram.id)) {
                Gui.showNotification('That promo code program has already been activated.');
            } else if (promoProgram) {
                this.activePromoProgramIds.push(promoProgram.id);
                this.trigger('update-rewards');
            } else if (code in this.bookedCouponCodes) {
                Gui.showNotification('That coupon code has already been scanned and activated.');
            } else {
                const programIdsWithScannedCoupon = Object.values(this.bookedCouponCodes).map(
                    (couponCode) => couponCode.program_id
                );
                const customer = this.get_client();
                const { successful, payload } = await rpc.query({
                    model: 'pos.config',
                    method: 'use_coupon_code',
                    args: [
                        [this.pos.config.id],
                        code,
                        this.creation_date,
                        customer ? customer.id : false,
                        programIdsWithScannedCoupon,
                    ],
                    kwargs: { context: session.user_context },
                });
                if (successful) {
                    this.bookedCouponCodes[code] = new CouponCode(code, payload.coupon_id, payload.program_id);
                    this.trigger('update-rewards');
                } else {
                    Gui.showNotification(payload.error_message);
                }
            }
        },

        _getNewRewardLines: async function () {
            const rewardsContainer = await this._calculateRewards();
            await this._setProgramIdsToGenerateCoupons(rewardsContainer);
            return [this._getLinesToAdd(rewardsContainer), rewardsContainer];
        },

        resetCoupons: async function (couponIds) {
            await rpc.query(
                {
                    model: 'coupon.coupon',
                    method: 'write',
                    args: [couponIds, { state: 'new' }],
                    kwargs: { context: session.user_context },
                },
                {}
            );
        },

        _getLinesToAdd: function (rewardsContainer) {
            this.assert_editable();
            return rewardsContainer
                .getAwarded()
                .map(({ product, unit_price, quantity, program, tax_ids, coupon_id }) => {
                    const options = {
                        quantity: quantity,
                        price: unit_price,
                        lst_price: unit_price,
                        is_program_reward: true,
                        program_id: program.id,
                        tax_ids: tax_ids,
                        coupon_id: coupon_id,
                    };
                    const line = new models.Orderline({}, { pos: this.pos, order: this, product });
                    this.fix_tax_included_price(line);
                    this.set_orderline_options(line, options);
                    return line;
                });
        },

        _setProgramIdsToGenerateCoupons: async function (rewardsContainer) {
            const programIdsToGenerateCoupons = [];
            for (let [program] of this._getActiveOnNextPromoPrograms()) {
                const { successful, reason } = await this._checkProgramRules(program);
                if (successful) {
                    programIdsToGenerateCoupons.push(program.id);
                } else {
                    const notAwarded = new Reward({ program, reason, awarded: false });
                    rewardsContainer.add([notAwarded]);
                }
            }
            this.programIdsToGenerateCoupons = programIdsToGenerateCoupons;
        },

        _calculateRewards: async function () {
            const rewardsContainer = new RewardsContainer();

            if (this._getRegularOrderlines().length === 0) {
                return rewardsContainer;
            }

            const {
                freeProductPrograms,
                fixedAmountDiscountPrograms,
                onSpecificPrograms,
                onCheapestPrograms,
                onOrderPrograms,
            } = await this._getValidActivePrograms(rewardsContainer);

            const collectRewards = (validPrograms, rewardGetter) => {
                const allRewards = [];
                for (let [program, coupon_id] of validPrograms) {
                    const [rewards, reason] = rewardGetter(program, coupon_id);
                    if (reason) {
                        const notAwarded = new Reward({ awarded: false, reason, program, coupon_id });
                        rewardsContainer.add([notAwarded]);
                    }
                    allRewards.push(...rewards);
                }
                return allRewards;
            };

            const freeProducts = collectRewards(freeProductPrograms, this._getProductRewards.bind(this));
            const fixedAmountDiscounts = collectRewards(fixedAmountDiscountPrograms, this._getFixedDiscount.bind(this));
            const specificDiscountGetter = (program, coupon_id) => {
                return this._getSpecificDiscount(program, coupon_id, freeProducts);
            };
            const specificDiscounts = collectRewards(onSpecificPrograms, specificDiscountGetter);
            const globalDiscounts = [];
            const onOrderDiscountGetter = (program, coupon_id) => {
                return this._getOnOrderDiscountRewards(program, coupon_id, freeProducts);
            };
            globalDiscounts.push(...collectRewards(onOrderPrograms, onOrderDiscountGetter));
            globalDiscounts.push(...collectRewards(onCheapestPrograms, this._getOnCheapestProductDiscount.bind(this)));

            // - Group the discounts by program id.
            const groupedGlobalDiscounts = {};
            for (let discount of globalDiscounts) {
                const key = [discount.program.id, discount.coupon_id].join(',');
                if (!(key in groupedGlobalDiscounts)) {
                    groupedGlobalDiscounts[key] = [discount];
                } else {
                    groupedGlobalDiscounts[key].push(discount);
                }
            }

            // - We select the group of discounts with highest total amount.
            // Note that the result is an Array that might contain more than one
            // discount lines. This is because discounts are grouped by tax.
            let currentMaxTotal = 0;
            let currentMaxKey = null;
            for (let key in groupedGlobalDiscounts) {
                const discountRewards = groupedGlobalDiscounts[key];
                const newTotal = discountRewards.reduce((sum, discReward) => sum + discReward.discountAmount, 0);
                if (newTotal > currentMaxTotal) {
                    currentMaxTotal = newTotal;
                    currentMaxKey = key;
                }
            }
            const theOnlyGlobalDiscount = currentMaxKey
                ? groupedGlobalDiscounts[currentMaxKey].filter((discountReward) => discountReward.discountAmount !== 0)
                : [];

            // - Get the messages for the discarded global_discounts
            if (theOnlyGlobalDiscount.length > 0) {
                const theOnlyGlobalDiscountKey = [
                    theOnlyGlobalDiscount[0].program.id,
                    theOnlyGlobalDiscount[0].coupon_id,
                ].join(',');
                for (let [key, discounts] of Object.entries(groupedGlobalDiscounts)) {
                    if (key !== theOnlyGlobalDiscountKey) {
                        const notAwarded = new Reward({
                            program: discounts[0].program,
                            coupon_id: discounts[0].coupon_id,
                            reason: 'Not the greatest global discount.',
                            awarded: false,
                        });
                        rewardsContainer.add([notAwarded]);
                    }
                }
            }

            rewardsContainer.add([
                ...freeProducts,
                ...fixedAmountDiscounts,
                ...specificDiscounts,
                ...theOnlyGlobalDiscount,
            ]);

//            Object.keys(rewardsContainer._rewards).forEach((value, index) => {
//                rewardsContainer._rewards[value].forEach((value_b, idx) => {
//                    if(value_b.product == undefined){
//                        rewardsContainer._rewards[value][idx].product = {};
//                    }
//                })
//            })

            return rewardsContainer;
        },

        _getValidActivePrograms: async function (rewardsContainer) {

            const freeProductPrograms = [],
                fixedAmountDiscountPrograms = [],
                onSpecificPrograms = [],
                onCheapestPrograms = [],
                onOrderPrograms = [];

            function updateProgramLists(program, coupon_id) {
                if (program.reward_type === 'product') {
                    freeProductPrograms.push([program, coupon_id]);
                } else {
                    if (program.discount_type === 'fixed_amount') {
                        fixedAmountDiscountPrograms.push([program, coupon_id]);
                    } else if (program.discount_apply_on === 'specific_products') {
                        onSpecificPrograms.push([program, coupon_id]);
                    } else if (program.discount_apply_on === 'cheapest_product') {
                        onCheapestPrograms.push([program, coupon_id]);
                    } else {
                        onOrderPrograms.push([program, coupon_id]);
                    }
                }
            }

            for (let [program, coupon_id] of this._getBookedPromoPrograms()) {
                // Booked coupons from on next order promo programs do not need
                // checking of rules because checks are done before generating
                // coupons.
                updateProgramLists(program, coupon_id);
            }

            for (let [program, coupon_id] of [
                ...this._getBookedCouponPrograms(),
                ...this._getActiveOnCurrentPromoPrograms(),
            ]) {
                const { successful, reason } = await this._checkProgramRules(program);
                if (successful) {
                    updateProgramLists(program, coupon_id);
                } else {
                    const notAwarded = new Reward({ program, coupon_id, reason, awarded: false });
                    rewardsContainer.add([notAwarded]);
                }
            }

            return {
                freeProductPrograms,
                fixedAmountDiscountPrograms,
                onSpecificPrograms,
                onCheapestPrograms,
                onOrderPrograms,
            };
        },
        _getAutomaticPromoProgramIds: function () {
            return this.pos.promo_programs
                .filter((program) => {
                    return program.promo_code_usage == 'no_code_needed';
                })
                .map((program) => program.id);
        },

        _getBookedCouponPrograms: function () {
            return Object.values(this.bookedCouponCodes)
                .map((couponCode) => [
                    this.pos.coupon_programs_by_id[couponCode.program_id],
                    parseInt(couponCode.coupon_id, 10),
                ])
                .filter(([program]) => {
                    return program.program_type === 'coupon_program';
                });
        },

        _getBookedPromoPrograms: function () {
            return Object.values(this.bookedCouponCodes)
                .map((couponCode) => [
                    this.pos.coupon_programs_by_id[couponCode.program_id],
                    parseInt(couponCode.coupon_id, 10),
                ])
                .filter(([program]) => {
                    return program.program_type === 'promotion_program';
                });
        },

        _getActiveOnCurrentPromoPrograms: function () {
            return this.activePromoProgramIds
                .map((program_id) => [this.pos.coupon_programs_by_id[program_id], null])
                .filter(([program]) => {
                    return program.promo_applicability === 'on_current_order';
                });
        },

        _getActiveOnNextPromoPrograms: function () {
            return this.activePromoProgramIds
                .map((program_id) => [this.pos.coupon_programs_by_id[program_id], null])
                .filter(([program]) => {
                    return program.promo_applicability === 'on_next_order';
                });
        },

        _checkProgramRules: async function (program) {
            const amountToCheck =
                program.rule_minimum_amount_tax_inclusion === 'tax_included'
                    ? this.get_total_with_tax()
                    : this.get_total_without_tax();
            if (!(amountToCheck >= program.rule_minimum_amount)) {
                return {
                    successful: false,
                    reason: 'Minimum amount for this program is not satisfied.',
                };
            }

            const validQuantity = this._getRegularOrderlines()
                .filter((line) => {
                    return program.valid_product_ids.has(line.product.id);
                })
                .reduce((total, line) => total + line.quantity, 0);
            if (!(validQuantity >= program.rule_min_quantity)) {
                return {
                    successful: false,
                    reason: "Program's minimum quantity is not satisfied.",
                };
            }

            if (program.program_type === 'coupon_program') {
                return {
                    successful: true,
                };
            }

            const customer = this.get_client();
            if (program.rule_partners_domain && !program.valid_partner_ids.has(customer ? customer.id : 0)) {
                return {
                    successful: false,
                    reason: "Current customer can't avail this program.",
                };
            }

            const ruleFrom = program.rule_date_from ? new Date(program.rule_date_from) : new Date(-8640000000000000);
            const ruleTo = program.rule_date_to ? new Date(program.rule_date_to) : new Date(8640000000000000);
            const orderDate = new Date();
            if (!(orderDate >= ruleFrom && orderDate <= ruleTo)) {
                return {
                    successful: false,
                    reason: 'Program already expired.',
                };
            }

            if (program.maximum_use_number !== 0) {
                const [result] = await rpc
                    .query({
                        model: 'coupon.program',
                        method: 'read',
                        args: [program.id, ['total_order_count']],
                        kwargs: { context: session.user_context },
                    })
                    .catch(() => Promise.resolve([false]));
                if (!result) {
                    return {
                        successful: false,
                        reason: 'Unable to get the number of usage of the program.',
                    };
                } else if (!(result.total_order_count < program.maximum_use_number)) {
                    return {
                        successful: false,
                        reason: "Program's maximum number of usage has been reached.",
                    };
                }
            }

            return {
                successful: true,
            };
        },

        _getProductRewards: function (program, coupon_id) {
            const totalQuantity = this._getRegularOrderlines()
                .filter((line) => {
                    return program.valid_product_ids.has(line.product.id);
                })
                .reduce((quantity, line) => quantity + line.quantity, 0);

            const freeQuantity = computeFreeQuantity(
                totalQuantity,
                program.rule_min_quantity,
                program.reward_product_quantity
            );
            if (freeQuantity === 0) {
                return [[], 'Zero free product quantity.'];
            } else {
//                const rewardProduct = this.pos.db.get_product_by_id(program.reward_product_id[0]);
                Object.filter = (obj, predicate) =>
                    Object.keys(obj)
                          .filter( key => predicate(obj[key]) )
                          .reduce( (res, key) => (res[key] = obj[key], res), {} );
                let producto_dscto = Object.filter(this.pos.db.product_by_id, e => e.desc_pos == true);

                const rewardProduct = this.pos.db.get_product_by_id(Object.keys(producto_dscto)[0]);

//                const discountLineProduct = this.pos.db.get_product_by_id(program.discount_line_product_id[0]);
                const discountLineProduct = this.pos.db.get_product_by_id(Object.keys(producto_dscto)[0]);
                console.log('discountLineProduct =>', discountLineProduct)
                return [
                    [
                        new Reward({
                            product: discountLineProduct,
                            unit_price: -rewardProduct.lst_price,
                            quantity: freeQuantity,
                            program: program,
                            tax_ids: rewardProduct.taxes_id,
                            coupon_id: coupon_id,
                        }),
                    ],
                    null,
                ];
            }
        },

        _getFixedDiscount: function (program, coupon_id) {
            const discountAmount = Math.min(program.discount_fixed_amount, program.discount_max_amount || Infinity);
            Object.filter = (obj, predicate) =>
                    Object.keys(obj)
                          .filter( key => predicate(obj[key]) )
                          .reduce( (res, key) => (res[key] = obj[key], res), {} );
                let producto_dscto = Object.filter(this.pos.db.product_by_id, e => e.desc_pos == true);
            return [
                [
                    new Reward({
//                        product: this.pos.db.get_product_by_id(program.discount_line_product_id[0]),
                        product: this.pos.db.get_product_by_id(Object.keys(producto_dscto)[0]),
                        unit_price: -discountAmount,
                        quantity: 1,
                        program: program,
                        tax_ids: [],
                        coupon_id: coupon_id,
                    }),
                ],
                null,
            ];
        },

        _getSpecificDiscount: function (program, coupon_id, productRewards) {
            const productIdsToAccount = new Set();
            const amountsToDiscount = {};
            for (let line of this._getRegularOrderlines()) {
                if (program.discount_specific_product_ids.has(line.get_product().id)) {
                    const key = this._getGroupKey(line);
                    if (!(key in amountsToDiscount)) {
                        amountsToDiscount[key] = line.get_quantity() * line.get_lst_price();
                    } else {
                        amountsToDiscount[key] += line.get_quantity() * line.get_lst_price();
                    }
                    productIdsToAccount.add(line.get_product().id);
                }
            }
            this._considerProductRewards(amountsToDiscount, productIdsToAccount, productRewards);
            return this._createDiscountRewards(program, coupon_id, amountsToDiscount);
        },

        _getOnCheapestProductDiscount: function (program, coupon_id) {
            const amountsToDiscount = {};
            const orderlines = this._getRegularOrderlines();
            if (orderlines.length > 0) {
                const cheapestLine = orderlines.reduce((min_line, line) => {
                    if (line.get_lst_price() < min_line.get_lst_price()) {
                        return line;
                    } else {
                        return min_line;
                    }
                }, orderlines[0]);
                const key = this._getGroupKey(cheapestLine);
                amountsToDiscount[key] = cheapestLine.get_lst_price();
            }
            return this._createDiscountRewards(program, coupon_id, amountsToDiscount);
        },

        _getOnOrderDiscountRewards: function (program, coupon_id, productRewards) {
            const productIdsToAccount = new Set();
            const amountsToDiscount = {};
            for (let line of this._getRegularOrderlines()) {
                const key = this._getGroupKey(line);
                if (!(key in amountsToDiscount)) {
                    amountsToDiscount[key] = line.get_quantity() * line.get_lst_price();
                } else {
                    amountsToDiscount[key] += line.get_quantity() * line.get_lst_price();
                }
                productIdsToAccount.add(line.get_product().id);
            }
            this._considerProductRewards(amountsToDiscount, productIdsToAccount, productRewards);
            return this._createDiscountRewards(program, coupon_id, amountsToDiscount);
        },

        _considerProductRewards: function (amountsToDiscount, productIdsToAccount, productRewards) {
            for (let reward of productRewards) {
                if (reward.rewardedProductId && productIdsToAccount.has(reward.rewardedProductId)) {
                    const key = reward.tax_ids.join(',');
                    amountsToDiscount[key] += reward.quantity * reward.unit_price;
                }
            }
        },
        _getGroupKey: function (line) {
            return line
                .get_taxes()
                .map((tax) => tax.id)
                .join(',');
        },
        _createDiscountRewards: function (program, coupon_id, amountsToDiscount) {
            const discountRewards = Object.entries(amountsToDiscount).map(([tax_keys, amount]) => {
                let discountAmount = (amount * program.discount_percentage) / 100.0;
                discountAmount = Math.min(discountAmount, program.discount_max_amount || Infinity);

                Object.filter = (obj, predicate) =>
                    Object.keys(obj)
                          .filter( key => predicate(obj[key]) )
                          .reduce( (res, key) => (res[key] = obj[key], res), {} );
                let producto_dscto = Object.filter(this.pos.db.product_by_id, e => e.desc_pos == true);

                return new Reward({
//                    product: this.pos.db.get_product_by_id(program.discount_line_product_id[0]),
                    product: this.pos.db.get_product_by_id(Object.keys(producto_dscto)[0]),
                    unit_price: -discountAmount,
                    quantity: 1,
                    program: program,
                    tax_ids: tax_keys !== '' ? tax_keys.split(',').map((val) => parseInt(val, 10)) : [],
                    coupon_id: coupon_id,
                });
            });
            return [discountRewards, discountRewards.length > 0 ? null : 'No items to discount.'];
        },
    });

    var _orderline_super = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_as_JSON: function () {
            var result = _orderline_super.export_as_JSON.apply(this);
            result.is_program_reward = this.is_program_reward;
            result.program_id = this.program_id;
            result.coupon_id = this.coupon_id;
            return result;
        },
        init_from_JSON: function (json) {
            if (json.is_program_reward) {
                this.is_program_reward = json.is_program_reward;
                this.program_id = json.program_id;
                this.coupon_id = json.coupon_id;
                this.tax_ids = json.tax_ids[0][2];
            }
            _orderline_super.init_from_JSON.apply(this, [json]);
        },
        set_quantity: function (quantity, keep_price) {
            _orderline_super.set_quantity.apply(this, [quantity, keep_price]);
            if (quantity === 'remove' && this.is_program_reward) {
                let related_rewards = this.order.orderlines.filter(
                    (line) => line.is_program_reward && line.program_id === this.program_id
                );
                for (let line of related_rewards) {
                    line.order.remove_orderline(line);
                }
                if (related_rewards.length !== 0) {
                    Gui.showNotification('Other reward lines from the same program were also removed.');
                }
            }
        },
    });
});
