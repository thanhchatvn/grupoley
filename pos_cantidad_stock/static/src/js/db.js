odoo.define('pos_cantidad_stock.DB', function (require) {
    "use strict";

    var db = require('point_of_sale.DB');
    var utils = require('web.utils');
    var _super_db = db.prototype;

    _super_db.get_product_by_category = function(category_id, porExistencia){
        var product_ids  = this.product_by_category_id[category_id];
        var list = [];
        if (product_ids) {
            for (var i = 0, len = Math.min(product_ids.length, this.limit); i < len; i++) {
                if(porExistencia  == 1 && this.product_by_id[product_ids[i]].qty_available > 0){
                    list.push(this.product_by_id[product_ids[i]]);
                }else if(porExistencia  == 2 && this.product_by_id[product_ids[i]].qty_available == 0){
                    list.push(this.product_by_id[product_ids[i]]);
                }else if (porExistencia  == 0){
                    list.push(this.product_by_id[product_ids[i]]);
                }
            }
        }
        return list;
    };

    _super_db.search_product_in_category = function(category_id, query, porExistencia){
        try {
            query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
            query = query.replace(/ /g,'.+');
            var re = RegExp("([0-9]+):.*?"+utils.unaccent(query),"gi");
        }catch(e){
            return [];
        }
        var results = [];
        for(var i = 0; i < this.limit; i++){
            var r = re.exec(this.category_search_string[category_id]);
            if(r){
                var id = Number(r[1]);
                const temp_product = this.get_product_by_id(id);
                if(porExistencia == 0){
                    results.push(temp_product);
                }else if(porExistencia == 1 && temp_product.qty_available > 0){
                    results.push(temp_product);
                }else if(porExistencia == 2 && temp_product.qty_available == 0){
                    results.push(temp_product);
                }
            }else{
                break;
            }
        }
        return results;
    }

});