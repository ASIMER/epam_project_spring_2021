$(document).ready(function () {
    $.ajax({
        url: "/employee_crud",
        dataType: "json",
        data: {"employee_id": employee_id},
        type: "GET",
        success: function (response) {
            let employee = response["data"][0]
            $("#employee_name").val(employee["0"])
            $("#date_of_birth").val(employee["1"])
            $("#salary").val(employee["2"])
            $("#department_name").val(employee["3"])
        },
        error: function (response) {
            alert(response.responseText)
            $("#all_content").html("Wrong employee id. Open employees page: <a href='" + employees_address + "'>redirect</a>")
        }});
    let send_btn = $("#insert_btn")

    // Delete button function with ajax query
    $('#delete_button').click(function () {
        let data = JSON.stringify({'data': [employee_id]})
        $.ajax({
            url: "/employee_crud",
            dataType: "json",
            data: data,
            'contentType': "application/json; charset=UTF-8",
            type: "DELETE",
            success: function (response) {
                console.log(response.responseText)
                $("#all_content").html("Employee has been deleted. Open employees page: <a href='" + employees_address + "'>redirect</a>")
            },
            error: function (response) {
                alert(response.responseText)
            }
        })
    });

    // Update button function
    $('#update_button').click(function () {
        $("#insert_btn").attr("id", "send_update");
        $("#form_title").text('Enter new values for this employee')
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
                    alert(response['Message'])
                },
                error: function (response) {
                    alert(response.responseText)
                }
            })
        } else {
            // Update query
            $.ajax({
                url: "/employee_crud",
                dataType: "json",
                data: form,
                type: "PUT",
                success: function (response) {
                    alert(response)
                    $("#send_update").attr("id", "insert_btn");
                    $("#form_title").text('Create a copy of the employee')
                },
                error: function (response) {
                    alert(response.responseText)
                }
            })
        }
    });
});