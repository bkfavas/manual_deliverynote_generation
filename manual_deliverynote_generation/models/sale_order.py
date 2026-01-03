# -*- coding: utf-8 -*-
# File: models/sale_manual_delivery.py

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manual_delivery_allowed = fields.Boolean(
        string="Manual Delivery Allowed",
        compute='_compute_manual_delivery_allowed',
        store=True,  # 👈 Add this
        help="True if delivery can be manually created (confirmed order + no active pickings)."
    )
    manual_delivery_created = fields.Boolean(
        string="Manual Delivery Created",
        default=False,
        copy=False,
        help="Indicates if a delivery was manually created for this order."
    )

    @api.depends('state', 'picking_ids.state')
    def _compute_manual_delivery_allowed(self):
        for order in self:
            # Only allow manual delivery creation if:
            # - Order is confirmed (sale/done), AND
            # - There are NO pickings in states other than 'cancel' or 'done'
            if order.state not in ['sale', 'done']:
                order.manual_delivery_allowed = False
            else:
                active_pickings = order.picking_ids.filtered(
                    lambda p: p.state not in ('cancel', 'done')
                )
                # If no active (non-cancelled, non-done) pickings exist → allow re-creation
                order.manual_delivery_allowed = not bool(active_pickings)

    def copy(self, default=None):
        """
        When duplicating a sale order, reset manual_delivery_created to False
        so the new order behaves like a fresh one.
        """
        default = dict(default or {})
        # Ensure manual_delivery_created is reset on copy
        default.setdefault('manual_delivery_created', False)
        # Also reset procurement_group_id and picking_ids to avoid conflicts
        default.setdefault('procurement_group_id', False)
        # Note: picking_ids is a One2many, so it won't be copied anyway, but just to be safe
        return super(SaleOrder, self).copy(default)

    def action_confirm(self):
        """
        Confirm SO without auto-creating delivery.
        We pass a context flag that our SOL overrides will use to skip stock/procurement rules.
        """
        _logger.debug('SaleOrder.action_confirm called with skip_auto_delivery=True on %s', self.ids)
        return super(SaleOrder, self.with_context(skip_auto_delivery=True)).action_confirm()

    def create_delivery_note_manually(self):
        for order in self:
            if order.state not in ['sale', 'done']:
                raise UserError(_('You can only create delivery notes for confirmed sales orders.'))

            existing_pickings = order.picking_ids.filtered(lambda p: p.state not in ['cancel', 'done'])
            if existing_pickings:
                raise UserError(_('Active delivery orders already exist for this sale order.'))

            if not order.procurement_group_id:
                vals = order._prepare_procurement_group_vals()
                order.procurement_group_id = self.env['procurement.group'].create(vals)

            deliverable_lines = order.order_line.filtered(
                lambda l: l.product_id
                and l.product_id.type == 'product'
                and l.product_uom_qty > 0
                and l.state in ('sale', 'done')
            )
            if not deliverable_lines:
                raise UserError(_('No deliverable (stockable) products with positive quantities found.'))

            deliverable_lines.with_context(manual_delivery_override=True)._action_launch_stock_rule()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }



    def action_view_delivery_pickings(self):
        """Open the delivery pickings related to the SO."""
        self.ensure_one()
        pickings = self.picking_ids.filtered(lambda p: p.state != 'cancel')

        if not pickings:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Deliveries'),
                    'message': _('No delivery orders found.'),
                    'type': 'info',
                    'sticky': False,
                }
            }

        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if len(pickings) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': pickings.id,
                'views': [(False, 'form')],
            })
        else:
            action['domain'] = [('id', 'in', pickings.ids)]
        return action

    def _prepare_procurement_group_vals(self):
        """Prepare values for procurement group creation."""
        self.ensure_one()
        return {
            'name': self.name,
            'move_type': self.picking_policy,
            'sale_id': self.id,
            'partner_id': self.partner_shipping_id.id,
        }
    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Only skip stock rule if:
        - Order is confirmed AND NOT manual override
        - AND the route is NOT "Buy"
        """
        BUY_ROUTE_XML_ID = 'purchase_stock.route_warehouse_buy'
        buy_route = self.env.ref(BUY_ROUTE_XML_ID, raise_if_not_found=False)

        allowed_lines = self.env['sale.order.line']
        for line in self:
            if line.order_id.state in ('sale', 'done') and not line.env.context.get('manual_delivery_override'):
                # Get all routes (product + category)
                routes = line.product_id.route_ids | line.product_id.categ_id.total_route_ids
                if buy_route and buy_route in routes:
                    _logger.debug('SOL %s: Allowing Buy route procurement (auto-PO).', line.id)
                    allowed_lines |= line
                    continue
                else:
                    _logger.debug('SOL %s: Skipping non-Buy route.', line.id)
                    continue
            allowed_lines |= line

        if not allowed_lines:
            return

        return super(SaleOrderLine, allowed_lines)._action_launch_stock_rule(previous_product_uom_qty)

    def _action_launch_procurement_rule(self, previous_product_uom_qty=False):
        # Same logic for legacy method
        allowed_lines = self.env['sale.order.line']
        for line in self:
            if line.order_id.state in ('sale', 'done') and not line.env.context.get('manual_delivery_override'):
                _logger.debug('Skipping _action_launch_procurement_rule for SOL %s: order confirmed and not in manual delivery mode', line.id)
                continue
            allowed_lines |= line

        if not allowed_lines:
            return

        return super(SaleOrderLine, allowed_lines)._action_launch_procurement_rule(previous_product_uom_qty)
    

