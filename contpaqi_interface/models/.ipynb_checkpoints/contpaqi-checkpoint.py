# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from datetime import datetime
import pymssql
from odoo.exceptions import UserError


class contpaqi_interface(models.Model):
    _name = 'contpaqi.interface'
    _description = 'Interfaz de CONTPAQi'
    _rec_name = 'reference'

    # ---------------------------------------------------------------------------------------------------------
    #                                    FUNCIONES PARA OBTENER DEFAULTS
    # ---------------------------------------------------------------------------------------------------------


    # ---------------------------------------------------------------------------------------------------------
    #                                        CAMPOS DEL MODELO
    # ---------------------------------------------------------------------------------------------------------

    initial_values = fields.Text(string='Inicializacion de valores', compute='_get_initial_values',
                                 store=True,readonly=True)
    initial_counter = fields.Boolean(string='Contador de actulización', store=True)
    period_type = fields.Many2one('period.type', string='Tipo de periodo',
                                  readonly=False, store=True)
    number_period = fields.Many2one('period.number', string='Periodo', compute='_get_period_number',
                                    readonly=False, store=True)
    accounting_year = fields.Many2one('account.year', string='Ejercicio',
                                      readonly=False, store=True)
    initial_date = fields.Date(string='Fecha Inicial', compute='_get_period_dates',
                               readonly=True, store=True)
    end_date = fields.Date(string='Fecha Final', readonly=True, store=True)
    status = fields.Char(string='Estatus', store=True)
    lot_id = fields.Char(string='ID Lote', required=True, store=True)
    reference = fields.Char(string='Referencia', required=True,store=True)
    accounting_policy_date = fields.Date(string='Fecha Poliza',required=True, store=True)
    journal_line_ids = fields.One2many('contpaq.payroll.line', 'payroll_id', store=True)
    period = fields.Char(string='Periodo', compute='_get_period', store=True)
    credit_sum = fields.Float(string='Abono', digits=(8,2), store=True, readonly=True)
    debit_sum = fields.Float(string='Cargo', digits=(8,2), store=True, readonly=True)
    button_method = fields.Boolean(string='Generar Poliza',store=True)
    button_create = fields.Boolean(string='Generar Asiento Contable',store=True)
    initialization = fields.Many2one(string='period.type',store=True)


    # ---------------------------------------------------------------------------------------------------------
    #                                            METODOS
    # ---------------------------------------------------------------------------------------------------------
    def server_connection(self):
        servidor = 'grupoley.com\CONTPAQ'
        db = str(self.env.company.x_company_payroll_db).strip()
        user = 'sa'
        passwo = 'syssql'

        try:
            connection = pymssql.connect(server=servidor, user=user, password=passwo, database=db)
            print('Conexion exitosa server_connection')
            return connection
        except Exception as e:
            print('No se establecio conexion', e)

    @api.onchange('initialization')
    def _get_initial_values(self):
        period_type = self.period_type
        print(self.period_type)

        print(self.env.company)
        try:
            for rec in self:
                if self.initial_counter == False:
                    self.env['period.type'].get_period_type()
                    self.period_type = period_type
                    self.env['account.year'].get_account_year()
                    self.initial_counter = True
                else:
                    pass
                rec.initial_values = 'Exito'

        except Exception as e:
            rec.initial_values = 'Fracaso'
            print('No es posible realizar la consulta en el metodo [_get_initial_values]: ', e)

    @api.onchange('period_type')
    def _get_period_number(self):
        try:
            initial_date = self.initial_date
            end_date = self.end_date
            initial_counter = self.initial_counter
            accounting_year = self.accounting_year
            status = self.status
            lot_id = self.lot_id
            reference = self.reference
            accounting_policy_date = self.accounting_policy_date
            self.period_type = self.env['period.number']._get_period_number(self.period_type)
            self.initial_date = initial_date
            self.end_date = end_date
            self.initial_counter = initial_counter
            self.accounting_year = accounting_year
            self.status = status
            self.lot_id = lot_id
            self.reference = reference
            self.accounting_policy_date = accounting_policy_date
        except Exception as e:
            print(e)

    @api.onchange('number_period', 'accounting_year', 'period_type')
    def _get_period_dates(self):
        for rec in self:
            try:
                rec.ensure_one()
                connection = self.server_connection()
                with connection.cursor() as cursor:
                    cursor.execute("""
                            Select Convert(char(101),p.FechaInicio,103) as DateIni,Convert(char(101),p.FechaFin,103) as DateFin
                            from nom10023 q (nolock)
                            inner join Nom10002 p (nolock) on q.idtipoperiodo=p.idtipoperiodo And p.numeroperiodo =""" + str(
                        rec.number_period.name) +
                                   """and p.ejercicio=""" + str(rec.accounting_year.name) +
                                   """where q.idtipoperiodo=""" + str(rec.period_type.code))
                    batchs = cursor.fetchall()
                    for batch in batchs:
                        initial_date = batch[0].strip()
                        end_date = batch[1].strip()
                        initial_date = datetime.strptime(initial_date, '%d/%m/%Y')
                        end_date = datetime.strptime(end_date, '%d/%m/%Y')
                        rec.initial_date = initial_date
                        rec.end_date = end_date

            except Exception as e:
                rec.initial_date = ''
                rec.end_date = ''
                print('No es posible realizar la consulta get period dates', e)


    @api.onchange('number_period', 'accounting_year', 'period_type')
    def _get_period(self):
        for rec in self:
            try:
                connection = self.server_connection()
                with connection.cursor() as cursor:
                    cursor.execute("""Select IdPeriodo from nom10002(nolock)
                                                    where idtipoperiodo=""" + str(rec.period_type.code).strip() +
                                   """and numeroperiodo=""" + str(rec.number_period.name).strip() +
                                   """ and ejercicio=""" + str(rec.accounting_year.name).strip())
                    batchs = cursor.fetchall()
                    for batch in batchs:
                        rec.period = str(batch[0]).strip()
            except Exception as e:
                rec.period = ''
                print('No es posible realizar la consulta get period', e)


    @api.onchange('period')
    def _get_concept_period(self):
        try:
            initial_date = self.initial_date
            end_date = self.end_date
            period_type = self.period_type
            number_period = self.number_period
            initial_counter = self.initial_counter
            accounting_year = self.accounting_year
            status = self.status
            lot_id = self.lot_id
            reference = self.reference
            accounting_policy_date = self.accounting_policy_date
            self.initial_date = initial_date
            self.end_date = end_date
            self.period = self.env['temporal.concepts']._get_concept_period(self.period)
            self.period_type = period_type
            self.number_period = number_period
            self.initial_counter = initial_counter
            self.accounting_year = accounting_year
            self.status = status
            self.lot_id = lot_id
            self.reference = reference
            self.accounting_policy_date = accounting_policy_date
        except Exception as e:
            print(e)

    @api.onchange('period')
    def _get_temporal_concept(self):
        try:
            initial_date = self.initial_date
            end_date = self.end_date
            period_type = self.period_type
            number_period = self.number_period
            initial_counter = self.initial_counter
            accounting_year = self.accounting_year
            status = self.status
            lot_id = self.lot_id
            reference = self.reference
            accounting_policy_date = self.accounting_policy_date
            period = self.period
            self.env['temporal.concepts.final']._get_temporal_concept()
            self.initial_counter = initial_counter
            self.initial_date = initial_date
            self.period_type = period_type
            self.number_period = number_period
            self.end_date = end_date
            self.accounting_year = accounting_year
            self.status = status
            self.lot_id = lot_id
            self.reference = reference
            self.accounting_policy_date = accounting_policy_date
            self.period = period
        except Exception as e:
            print(e)

    def generate_policy(self):
        print('Boton')
        try:
            if self.reference:
                period_type = self.period_type
                number_period = self.number_period
                initial_counter = self.initial_counter
                initial_date = self.initial_date
                end_date = self.end_date
                accounting_year = self.accounting_year
                status = self.status
                lot_id = self.lot_id
                reference = self.reference
                accounting_policy_date = self.accounting_policy_date
                period = self.period
                self.env['contpaq.policy']._generate_policy()
                self.period_type = period_type
                self.number_period = number_period
                self.initial_counter = initial_counter
                self.initial_date = initial_date
                self.end_date = end_date
                self.accounting_year = accounting_year
                self.status = status
                self.lot_id = lot_id
                self.reference = reference
                self.accounting_policy_date = accounting_policy_date
                self.period = period
                self.set_policy()
        except Exception as e:
            print(e)

    def set_policy(self):
        policy_obj = self.env['contpaq.policy'].search([('company_id', '=', self.env.company.id)])
        try:
            move_line = []
            debit_credit_list = []
            for rec in policy_obj:
                if rec.naturaleza == 'Cargo':
                    debit_credit_list.append(rec)
                    for credit in policy_obj:
                        if credit.naturaleza == 'Abono':
                            if (rec.importe == credit.importe and
                                rec.tipo == credit.tipo and
                                rec.descripcion == credit.descripcion and
                                rec.id_empleado == credit.id_empleado):
                                debit_credit_list.append(credit)
                                break

            for rec in debit_credit_list:
                if len(self.journal_line_ids) > 0:
                    self.journal_line_ids.unlink()
                    self.debit_sum = 0
                    self.credit_sum = 0

                if rec.naturaleza == 'Cargo':
                    cargo = rec.importe
                    self.debit_sum += float(cargo)
                    abono = '0'
                else:
                    cargo = '0'
                    abono = rec.importe
                    self.credit_sum += float(abono)
                data = {
                    'account' : rec.cuenta,
                    'description' : rec.descripcion_concepto,
                    'debit' : cargo,
                    'credit' : abono
                }

                move_line.append((0,0,data))
            self.journal_line_ids = move_line
        except Exception as e:
            print(e)

    def save_policy(self):
        self.validate_policy()
        for rec in self.journal_line_ids:
            if rec.analytic_account_id:
                analytic_account = rec.analytic_account_id.id
            else:
                analytic_account = None
            if float(rec.debit) > 0:
                if rec.account_debit:
                    account = rec.account_debit.id
                    account1 = rec.account_credit.id
                else:
                    error = ("El concepto: [{}] no tiene cuenta afectable").format(rec.description)
                    raise UserError(_(error))
            elif float(rec.credit) > 0:
                if rec.account_credit:
                    account = rec.account_debit.id
                    account1 = rec.account_credit.id
                else:
                    error = ("El concepto: [{}] no tiene cuenta afectable").format(rec.description)
                    raise UserError(_(error))
            else:
                error = ("El concepto: [{}] no tiene cargo o abono").format(rec.description)
                raise UserError(_(error))

        if self.reference:
            account_journal_obj = self.env['account.move']
            account_journal_lines_obj = self.env['account.move.line']
            data = {
                'name' : self.lot_id,
                'ref' : self.reference,
                'date' : self.accounting_policy_date,
                'payroll_policy' : True,
            }
            account_jorunal_id = account_journal_obj.create(data)
            for rec in self.journal_line_ids:

                if rec.analytic_account_id:
                    analytic_account = rec.analytic_account_id.id
                else:
                    analytic_account = None
                if float(rec.debit) > 0:
                    if rec.account_debit:
                        account = rec.account_debit.id
                        account1 = rec.account_credit.id
                    else:
                        error = ("El concepto: [{}] no tiene cuenta afectable").format(rec.description)
                        raise UserError(_(error))
                elif float(rec.credit) > 0:
                    if rec.account_credit:
                        account = rec.account_debit.id
                        account1 = rec.account_credit.id
                    else:
                        error = ("El concepto: [{}] no tiene cuenta afectable").format(rec.description)
                        raise UserError(_(error))
                else:
                    error = ("El concepto: [{}] no tiene cargo o abono").format(rec.description)
                    raise UserError(_(error))

                data = {
                    'move_id' : account_jorunal_id.id,
                    'name' : rec.description,
                    'account_id' : account,
                    'analytic_account_id' : analytic_account,
                    'currency_id' : self.env.company.currency_id.id,
                    'debit' : float(rec.debit),
                    'credit' : float(rec.credit)
                }
                data2 = {
                    'move_id': account_jorunal_id.id,
                    'name': rec.description,
                    'account_id': account1,
                    'analytic_account_id': analytic_account,
                    'currency_id': self.env.company.currency_id.id,
                    'debit': float(rec.credit),
                    'credit': float(rec.debit),
                }
                if float(rec.debit) > 0:
                    account_journal_lines_obj.create((data,data2))
    

    def validate_policy(self):
        duplicated_entry = self.env['account.move'].search([
            '&','&','&',
            ('payroll_policy','=',True),
            ('ref','=', self.reference),
            ('name','=',self.lot_id),
            ('date','=',self.accounting_policy_date)
        ])
        if len(duplicated_entry) > 0:
            raise UserError(_('Ya se encuentra interfazado'))