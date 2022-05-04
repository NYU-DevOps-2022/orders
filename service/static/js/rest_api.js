$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_order_data(res) {
        $("#order_id").val(res.id);
        $("#order_customer").val(res.customer_id);

        let ts = Date.parse(res.date_order);
        let nd = new Date(ts);
        let month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];

        let date_order = nd.getFullYear() + '-' + month[nd.getMonth()] + '-' + (nd.getDate()).toString().padStart(2, "0");

        $("#order_date").val(date_order);
    }

    function update_form_item_details(res) {
        $("#order_id").val(res.id);
        $("#order_customer").val(res.customer_id);

        let ts = Date.parse(res.date_order);
        let nd = new Date(ts);
        let month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];

        let date_order = nd.getFullYear() + '-' + month[nd.getMonth()] + '-' + (nd.getDate()).toString().padStart(2, "0");

        $("#order_date").val(date_order);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val("");
        $("#order_customer").val("");
        $("#order_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an Order
    // ****************************************

    $("#create-btn").click(function () {

        let customer = $("#order_customer").val();
        let date = $("#order_date").val();

        let data = {
            "customer_id": customer,
            "date_order": date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_order_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        let order_id = $("#order_id").val();
        let customer = $("#order_customer").val();
        let date = $("#order_date").val();

        let data = {
            "id": name,
            "customer_id": customer,
            "date_order": date,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_order_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}`,
            // contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_order_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/orders/${order_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for an Order
    // ****************************************

    $("#search-btn").click(function () {

        let customer = $("#order_customer").val();
        let date = $("#order_date").val();

        let queryString = ""

        if (customer) {
            queryString += 'customer_id=' + customer
        } else if (date) {
            queryString += 'date_order=' + date
        }
        console.log(date);
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders?${queryString}`,
            // contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Customer</th>'
            table += '<th class="col-md-2">Date</th>'
            table += '</tr></thead><tbody>'
            let firstOrder = "";
            for (let i = 0; i < res.length; i++) {
                let order = res[i];
                table += `<tr id="row_${i}"><td>${order.id}</td><td>${order.customer_id}</td><td>${order.date_order}</td></tr>`;
                if (i == 0) {
                    firstOrder = order;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstOrder != "") {
                update_form_order_data(firstOrder)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve order items
    // ****************************************

    //TODO: Test then hide/unhide tables.
    $("#retrieve-btn").click(function () {

        let order_id = $("#order_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/orders/${order_id}/items`,
            // contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#order_search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Customer</th>'
            table += '<th class="col-md-2">Date</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for (let i = 0; i < res.length; i++) {
                let item = res[i];
                table += `<tr id="row_${i}"><td>${item.product_id}</td><td>${item.product_price}</td><td>${item.product_quantity}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#order_search_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_form_order_data(firstItem)
            }

            update_form_item_details(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

})
