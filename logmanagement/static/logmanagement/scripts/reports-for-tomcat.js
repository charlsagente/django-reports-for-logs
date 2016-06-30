/**
 * Created by Charls on 09/06/2016.
 */
$(function () {

    var global_logs_values;
    var global_tomcat_values;

    $('#datetimepicker6').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    $('#datetimepicker7').datetimepicker({

        format: 'YYYY-MM-DD'
    });
    $("#datetimepicker6").on("dp.change", function (e) {
        $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
        $('#datetimepicker6').data("DateTimePicker").hide();
    });
    $("#datetimepicker7").on("dp.change", function (e) {
        $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
        $('#datetimepicker7').data("DateTimePicker").hide();
    });

    $('#myModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var log_level = button.data('log_level') // Extract info from data-* attributes
        var modal = $(this);

        $(modal.find('.modal-body table tbody')).empty();
        var files = {};
        for (var date in global_logs_values[log_level]) {
            for (var file in global_logs_values[log_level][date]) {
                if (files.hasOwnProperty(file))
                    files[file] = files[file].concat(global_logs_values[log_level][date][file]);
                else
                    files[file] = global_logs_values[log_level][date][file];
            }
        }

        for (var val in files) {
            modal.find('.modal-body table tbody').append(
                $('<tr>').append(
                    $('<td>').append(
                        $('<a>', {
                            href: val,
                            text: val,
                            target: "_blank"
                        })
                    )
                ).append(
                    $('<td>', {
                            text: files[val].length,
                            align: 'center'
                        }
                    )
                ).append(
                    $('<td>').append(
                        $('<textarea>', {
                            class: "form-control",
                            rows: "3",
                            text: files[val].join(", ")
                        })
                    )
                )
            );
        }
    });

    $('#tomcatModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var log_level = button.data('log_level') // Extract info from data-* attributes
        var modal = $(this);
        $(modal.find('.modal-body table tbody')).empty();

        for (var file in global_tomcat_values) {
            var arry = global_tomcat_values[file][log_level]
            modal.find('.modal-body table tbody').append(
                $('<tr>').append(
                    $('<td>').append(
                        $('<a>', {
                            href: file,
                            text: file,
                            target: "_blank"
                        })
                    )
                ).append(
                    $('<td>', {
                            text: global_tomcat_values[file][log_level].length,
                            align: 'center'
                        }
                    )
                ).append(
                    $('<td>').append(
                        $('<textarea>', {
                            class: "form-control",
                            rows: "3",
                            text: global_tomcat_values[file][log_level].join(", ")
                        })
                    )
                )
            );
        }
    });

    $('#btnsubmit').on('click', function (e) {
        $(this).html('<i class="fa fa-circle-o-notch fa-spin"></i> Espere..');
        $(this).attr('disabled', true);

        $.ajax({
            type: "GET",
            url:  $("#start_date").val() + "/" + $("#end_date").val(),

            success: function (data) {

                console.log(data);
                global_logs_values = data.files;
                global_tomcat_values = data.tomcat;

                $('table thead tr:nth-child(2)').empty();
                $('table tbody tr').empty();


                for (var log_level in data.tomcat_logs) {
                    $('#table_errors_catalina thead tr:nth-child(2)').append(
                        $('<th>', {
                            text: log_level
                        })
                    )
                    var column_cter = 0;
                    for (var date in data.tomcat_logs[log_level]) {
                        column_cter += text = data.tomcat_logs[log_level][date]
                    }
                    $('#table_errors_catalina tbody tr').append(
                        $('<td>').append(column_cter > 0 ? $('<a>', {
                                href: "#",
                                "data-toggle": "modal", "data-target": "#myModal", "data-log_level": log_level,
                                text: column_cter
                            }) : 0
                        )
                    )

                }

                for (var file_name in data.tomcat) {
                    var column_cter = 0;

                    for (var log_level in data.tomcat[file_name]) {
                        $('#table_errors_tomcat thead tr:nth-child(2)').append(
                            $('<th>', {
                                text: log_level
                            })
                        )
                        column_cter += data.tomcat[file_name][log_level].length
                    }
                    $('#table_errors_tomcat tbody tr').append(
                        $('<td>').append(column_cter > 0 ? $('<a>', {
                                href: "#",
                                "data-toggle": "modal", "data-target": "#tomcatModal", "data-log_level": log_level,
                                text: column_cter
                            }) : 0
                        )
                    )

                }


                $('#btnsubmit').text('Buscar');
                $('#btnsubmit').removeAttr('disabled');

            },
            error: function () {
                alert("Error");
                $('#btnsubmit').text('Buscar');
                $('#btnsubmit').removeAttr('disabled');
            }
        });
    });
});