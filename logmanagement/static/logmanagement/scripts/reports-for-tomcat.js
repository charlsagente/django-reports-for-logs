/**
 * Created by Charls on 09/06/2016.
 */
$(function () {

    var global_logs_values;

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

        $.each(global_logs_values[log_level], function (index, val) {

            modal.find('.modal-body table tbody').append(
                $('<tr>').append(
                    $('<td>').append(
                        $('<a>', {
                            href: val,
                            target: "_blank",
                            text: val
                        })
                    )
                ).append(
                    $('<td>', {
                            html: '<strong>' + ctr_files.line_counters + '</strong>',
                            align: 'center'
                        }
                    )
                ).append(
                    $('<td>').append(
                        $('<textarea>', {
                            class: "form-control",
                            rows: "3",
                            text: ctr_files.lines.sort().join(", ")
                        })
                    )
                )
            );


        });


    });


    $('#btnsubmit').on('click', function (e) {
        $(this).html('<i class="fa fa-circle-o-notch fa-spin"></i> Espere..');
        $(this).attr('disabled', true);
        $('table').addClass('animated zoomOutRight');
        $('table').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
            function () {
                $('strong span').text("");
                $('table').removeClass('animated zoomOutRight');
            });

        $.ajax({
            type: "GET",
            url: "tomcat/"+$("#start_date").val() + "/" + $("#end_date").val(),

            success: function (data) {

                console.log(data);

                global_logs_values=data.files;
                $('table thead tr:nth-child(2)').empty();
                $('table tbody tr').empty();

                for (var log_level in data.tomcat_logs) {
                    $('table thead tr:nth-child(2)').append(
                        $('<th>',{
                            text:log_level
                        })
                    )
                }
                for (var log_level in data.tomcat_logs) {
                    var column_cter=0;
                    for(var date in data.tomcat_logs[log_level]){
                        column_cter+=text=data.tomcat_logs[log_level][date]
                    }
                    $('table tbody tr').append(
                        $('<td>').append(column_cter > 0 ? $('<a>',{
                            href:"#",
                            "data-toggle":"modal", "data-target":"#myModal", "log_level":log_level,
                                text:column_cter
                        }): 0
                        )
                    )

                    //console.log(key, yourobject[key]);
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