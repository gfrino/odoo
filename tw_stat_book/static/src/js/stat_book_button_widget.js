/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

/**
 * Widget pulsante per aggiungere dati statistici da altri moduli
 * Questo widget può essere aggiunto a qualsiasi vista form in Odoo
 */
export class StatBookButtonWidget extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
    }

    async onClick() {
        // Ottieni il valore da aggiungere (puoi personalizzare la logica)
        const record = this.props.record;
        const value = this.calculateValue(record);

        // Apri il wizard per selezionare divisione/dipartimento
        const wizardAction = await this.orm.call(
            "stat.book.add.data.wizard",
            "open_wizard_from_record",
            [],
            {
                res_model: record.resModel,
                res_id: record.resId,
                value: value,
            }
        );

        this.action.doAction(wizardAction);
    }

    calculateValue(record) {
        // Logica per calcolare il valore dal record
        // Questa è una logica di esempio, andrà personalizzata per ogni modulo
        
        // Per i pagamenti potrebbe essere:
        if (record.data.amount) {
            return record.data.amount;
        }
        
        // Per le vendite potrebbe essere:
        if (record.data.amount_total) {
            return record.data.amount_total;
        }
        
        // Valore di default
        return 0.0;
    }
}

StatBookButtonWidget.template = "tw_stat_book.StatBookButtonWidget";
StatBookButtonWidget.props = {
    record: Object,
    string: { type: String, optional: true },
};

registry.category("fields").add("stat_book_button", StatBookButtonWidget);
