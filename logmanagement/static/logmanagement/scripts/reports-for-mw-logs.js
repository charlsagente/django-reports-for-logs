/**
 * Created by Charls on 09/06/2016.
 */
$(function () {
    $("#table-web-pt-errors").hide();
    $("#table-android-pt-errors").hide();
    $("#table-ios-pt-errors").hide();
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
        var recipient = button.data('loglist') // Extract info from data-* attributes
        var device_type = button.data('device-type');
        list = recipient.split(",")

        var modal = $(this);


        $(modal.find('.modal-body table tbody')).empty();

        $.each(list, function (index, val) {
            var ctr_files = {};
            if (global_logs_values[device_type].hasOwnProperty(val))
                ctr_files = global_logs_values[device_type][val];
            else
                ctr_files = {'line_counters': 0, 'lines': [0]};

            modal.find('.modal-body table tbody').append(
                $('<tr>').append(
                    $('<td>').append(
                        $('<a>', {
                            href: "showlog/"+val,
                            target: "_blank",
                            text: val
                        })
                    )
                ).append(
                    $('<td>', {
                            html: '<strong>' + ctr_files.line_counters + '</strong>',
                            class: 'cell_align'
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
        $('strong span').addClass('animated zoomOutRight');
        $('strong span').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
            function () {
                $('strong span').text("");
                $('strong span').removeClass('animated zoomOutRight');
            });

        var path_name=window.location.pathname;

        $.ajax({
            type: "GET",
            url: path_name+$("#start_date").val() + "/" + $("#end_date").val(),

            success: function (data) {

                console.log(data);
                global_logs_values = data['counter_errors_each_file'];
                $('#internal_errors_mw').text(data['internal-errors-mw-int']);
                $('#errors_mw').text(data['errors-mw-int']);

                $('#avg_time_android').text(data['sndrcvmsgs']['A']['avg_time'] + " s");
                $('#success_attended_android').text(data['sndrcvmsgs']['A']['success_attended']);
                $('#structure_errors_android').text(data['structure-mw']['A']);

                if (data['pathlogs']['A'].length > 0) {
                    $('#failed_attended_android').html(
                        '<a href="#" data-toggle="modal" data-target="#myModal" data-device-type="A" data-loglist="' +
                        data['pathlogs']['A'].sort().join() + '">' +
                        data['sndrcvmsgs']['A']['failed_attended'] + '</a>'
                    );
                }
                else {
                    $('#failed_attended_android').text(data['sndrcvmsgs']['A']['failed_attended']);
                }


                $('#avg_time_ios').text(data['sndrcvmsgs']['I']['avg_time'] + " s");
                $('#success_attended_ios').text(data['sndrcvmsgs']['I']['success_attended']);
                $('#structure_errors_ios').text(data['structure-mw']['I']);
                if (data['pathlogs']['I'].length > 0) {
                    $('#failed_attended_ios').html(
                        '<a href="#" data-toggle="modal" data-target="#myModal" data-device-type="I" data-loglist="' +
                        data['pathlogs']['I'].sort().join() + '">' +
                        data['sndrcvmsgs']['I']['failed_attended'] + '</a>'
                    );
                }
                else {
                    $('#failed_attended_ios').text(data['sndrcvmsgs']['I']['failed_attended']);
                }

                $('#avg_time_web').text(data['sndrcvmsgs']['W']['avg_time'] + " s");
                $('#success_attended_web').text(data['sndrcvmsgs']['W']['success_attended']);
                $('#structure_errors_web').text(data['structure-mw']['W']);
                if (data['pathlogs']['W'].length > 0) {
                    $('#failed_attended_web').html(
                        '<a href="#" data-toggle="modal" data-target="#myModal" data-device-type="W" data-loglist="' +
                        data['pathlogs']['W'].sort().join() + '">' +
                        data['sndrcvmsgs']['W']['failed_attended'] + '</a>'
                    );
                }
                else {
                    $('#failed_attended_web').text(data['sndrcvmsgs']['W']['failed_attended']);
                }

                $("#table-web-pt-errors").hide();
                $("#table-android-pt-errors").hide();
                $("#table-ios-pt-errors").hide();

                if(data['pt-internal-errors']['W'] && data['pt-internal-errors']['W'].length>0){
                    $("#table-web-pt-errors").show();
                    appendChilds( $("#table-web-pt-errors tbody"),data['pt-internal-errors']['W']);
                }
                if(data['pt-internal-errors']['A'] && data['pt-internal-errors']['A'].length>0){
                    $("#table-android-pt-errors").show();
                    appendChilds( $("#table-android-pt-errors tbody"),data['pt-internal-errors']['A']);
                }

                if(data['pt-internal-errors']['I'] && data['pt-internal-errors']['I'].length>0){
                    $("#table-ios-pt-errors").show();
                    appendChilds( $("#table-ios-pt-errors tbody"),data['pt-internal-errors']['I']);
                }


                function appendChilds(element,object){
                    $(element).empty();
                    $.each(object, function (index, val) {
                        $(element).append(
                            $('<tr>').
                                append($('<td>', {text: index + 1})).
                                append($('<td>', {text: val.date})).
                                append($('<td>', {text: val.error_type})).
                                append($('<td>', {text: val.service_id})).
                                append($('<td>', {text: val.class})).
                                append($('<td>', {text: val.file}))
                        );

                    });
                }


                $('strong span').addClass('animated bounceInLeft');
                $('strong span').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
                    function () {
                        $('strong span').removeClass('animated bounceInLeft');
                    });
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