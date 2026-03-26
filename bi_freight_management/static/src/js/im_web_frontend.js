/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.FreightManagement = publicWidget.Widget.extend({
    selector: '#booking_create',
    events: {
        "change .transport_check": "_onChange_Check_Input",
    },
    init: function (parent) {
        $('.shipping_ocean_type').hide();
        $('.shipping_air_type').hide();
        $('.shipping_land_type').hide();
        this._super(parent);
    },
    _onChange_Check_Input: function (ev) {

        var inputFieldGateway = document.getElementById("gateway_id");
        var inputFieldDestination = document.getElementById("destination_id");
        var inputFieldLoading = document.getElementById("loading_port_id");
        var inputFieldDischarge = document.getElementById("discharge_port_id");
        var inputFieldFcl = document.getElementById("fcl");
        var inputFieldFtl = document.getElementById("ftl");
        var inputFieldFromport = document.getElementById("from_port_id");
        var inputFieldToport = document.getElementById("to_port_id");

        inputFieldGateway.removeAttribute("required", true);
        inputFieldDestination.removeAttribute("required", true);
        inputFieldLoading.removeAttribute("required");
        inputFieldDischarge.removeAttribute("required");
        inputFieldFcl.removeAttribute("required");
        inputFieldFtl.removeAttribute("required");
        inputFieldFromport.removeAttribute("required");
        inputFieldToport.removeAttribute("required");

        if ($(ev.currentTarget).val() == 'ocean') {
            $('.shipping_ocean_type').show();
            $('.shipping_air_type').hide();
            $('.shipping_land_type').hide();

            inputFieldLoading.setAttribute("required", true);
            inputFieldDischarge.setAttribute("required", true);
            inputFieldFcl.setAttribute("required", true);
        } else if ($(ev.currentTarget).val() == 'air') {
            $('.shipping_ocean_type').hide();
            $('.shipping_air_type').show();
            $('.shipping_land_type').hide();

            inputFieldGateway.setAttribute("required", true);
            inputFieldDestination.setAttribute("required", true);
        } else if ($(ev.currentTarget).val() == 'land') {
            $('.shipping_ocean_type').hide();
            $('.shipping_air_type').hide();
            $('.shipping_land_type').show();

            inputFieldFromport.setAttribute("required", true);
            inputFieldToport.setAttribute("required", true);
            inputFieldFtl.setAttribute("required", true);
        } else {
            $('.shipping_ocean_type').hide();
            $('.shipping_air_type').hide();
            $('.shipping_land_type').hide();
        }
    },
}),
publicWidget.registry.FreightManagementBooking = publicWidget.Widget.extend({
    selector: '#booking_data',
    events: {
        "click .booking_create_btn": "_onClick_booking_create_btn",
    },
    init: function (parent) {
        $('.booking_create').hide();
        this._super(parent);
    },
    _onClick_booking_create_btn: function () {
        $('.booking_create').show();
        $('#booking_data').hide();
    },
})
