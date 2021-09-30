from typing import List
from odoo import models, fields
from datetime import timedelta, datetime
from odoo.addons.sale.models.sale import SaleOrder


class SaleOrderArchive(models.Model):
    _name = "sale.order.sale_order_archive"
    _description = "sale.order.sale_order_archive"

    # Most of fields are just copied from odoo/sale/models/sale.py
    # I just deleted kwargs I didn't find useful

    name = fields.Char(size=1234)
    order_create_date = fields.Datetime(
        string="Order Date",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
    )
    user_id = fields.Many2one(
        "res.users",
        string="SalePerson",
        index=True,
    )
    order_total_amount = fields.Monetary()
    currency_id = fields.Many2one(
        "res.currency",
        related="pricelist_id.currency_id",
        string="Currency",
        readonly=True,
        required=True,
    )
    count_of_order_lines = fields.Integer()

    def cron_delete_old_orders_and_create_order_archive_from_them(self):
        # From what I read cron are defined as methods like that and can be added in views
        # This is more like pseudocode

        cancel_date = datetime.today() - timedelta(days=30)
        # write_date seems to be build in
        orders_to_delete: List["SaleOrder"] = self.env["sale.order"].search(
            [("write_date", "<", cancel_date), ("state", "in", ["sale", "cancel"])]
        )
        # no idea if this is really list of [SaleOrder] but probably something iterable
        for order in orders_to_delete:
            archive_order = self.create(
                vals_list=[
                    {
                        "name": order.name,
                        "order_create_date": order.date_order,
                        "partner_id": order.partner_id,
                        "user_id": order.user_id,
                        "order_total_amount": order.amount_total,
                        "currency_id": order.currency_id,
                        "count_of_order_lines": len(
                            order.order_line
                        ),  # or anything which returns
                        # number of related order_line
                    }
                ]
            )
            order.unlink()
