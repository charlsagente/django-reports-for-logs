/**
 * Created by Charls on 09/06/2016.
 */
$(function () {
    $('#datetimepicker6').datetimepicker({
        format: 'YYYY-MM-DD'
    });
    $('#datetimepicker7').datetimepicker({
        useCurrent: false, //Important! See issue #1075
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


    $('#btnsubmit').on('click', function (e) {
        $.ajax({
            type: "GET",
            url: $("#start_date").val() + "/" + $("#end_date").val(),

            success: function (data) {

                console.log(data);
                $('#internal_errors_mw').text(data['internal-errors-mw-int']);
                $('#errors_mw').text(data['errors-mw-int']);

                $('#avg_time_android').text(data['sndrcvmsgs']['A']['avg_time']);
                $('#failed_attended_android').text(data['sndrcvmsgs']['A']['failed_attended']);
                $('#success_attended_android').text(data['sndrcvmsgs']['A']['success_attended']);

                $('#avg_time_ios').text(data['sndrcvmsgs']['I']['avg_time']);
                $('#failed_attended_ios').text(data['sndrcvmsgs']['I']['failed_attended']);
                $('#success_attended_ios').text(data['sndrcvmsgs']['I']['success_attended']);

                $('#avg_time_web').text(data['sndrcvmsgs']['W']['avg_time']);
                $('#failed_attended_web').text(data['sndrcvmsgs']['W']['failed_attended']);
                $('#success_attended_web').text(data['sndrcvmsgs']['W']['success_attended']);


            },
            error: function () {
                alert("Error");
            }
        });
    });
});