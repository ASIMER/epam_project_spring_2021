$(document).ready(function () {
    let selected = [];
    let send_btn = $("#insert_btn")

    // Datatable initialization
    let table = $("#data_table").DataTable({
        "ajax": "/employee_crud",
        "rowCallback": function (row, data) {
            if ($.inArray(data.DT_RowId, selected) !== -1) {
                $(row).addClass('selected');
            }
        }
    });

    // Select row function
    $('#data_table tbody').on('click', 'tr', function () {
        let id = this.id;
        let index = $.inArray(id, selected);

        if (index === -1) {
            selected.push(id);
        } else {
            selected.splice(index, 1);
        }

        $(this).toggleClass('selected');
    });

    // Delete button function with ajax query
    $('#delete_button').click(function () {
        let rows = table.rows('.selected');
        let data = JSON.stringify({'data': Array.from(rows.ids())})
        $.ajax({
            url: "/employee_crud",
            dataType: "json",
            data: data,
            'contentType': "application/json; charset=UTF-8",
            type: "DELETE",
            success: function (response) {
                console.log(response.responseText)
                rows.remove().draw(false)
            },
            error: function (response) {
                alert(response.responseText)
            }
        })
    });

    // Update button function
    $('#update_button').click(function () {
        let rows = table.rows('.selected');
        if (rows.length > 1) {
            alert('Select only one row!')
        } else {
            let selected_row = table.row('.selected')
            let row_id = selected_row.id()
            /* change id in send btn */
            $("#insert_btn").attr("id", "send_update");
            $("#form_title").text('Enter new values for this row')

            /* change form values to row data */
            $("#employee_name").val(selected_row.data()[0])
            $("#date_of_birth").val(selected_row.data()[1])
            $("#salary").val(selected_row.data()[2])
            $("#department_name").val(selected_row.data()[3])
            $("#employee_id").val(row_id)
        }
    });

    // Send insert/update ajax query
    $('#insert_form').submit(function (event) {
        event.preventDefault()
        let form = $("#insert_form").serialize();
        if (send_btn.attr("id") === "insert_btn") {
            // Insert query
            $.ajax({
                url: "/employee_crud",
                dataType: "json",
                data: form,
                type: "POST",
                success: function (response) {
                    table.row.add({
                            '0': $("#employee_name").val(),
                            '1': $("#date_of_birth").val(),
                            '2': $("#salary").val(),
                            '3': $("#department_name").val(),
                            'DT_RowId': response['id'],
                        }
                    ).draw(false);
                    alert(response['Message'])
                },
                error: function (response) {
                    alert(response.responseText)
                }
            })
        } else {
            // Update query
            let row_id = table.row('.selected').id()
            $.ajax({
                url: "/employee_crud",
                dataType: "json",
                data: form,
                type: "PUT",
                success: function (response) {
                    table.row('#' + row_id).data({
                            '0': $("#employee_name").val(),
                            '1': $("#date_of_birth").val(),
                            '2': $("#salary").val(),
                            '3': $("#department_name").val(),
                            'DT_RowId': row_id,
                        }
                    ).draw(false);
                    alert(response)
                    $("#send_update").attr("id", "insert_btn");
                    $("#form_title").text('Insert new employee')
                },
                error: function (response) {
                    alert(response.responseText)
                }
            })
        }
    });
});