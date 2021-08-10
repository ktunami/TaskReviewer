$(function(){
    const timestamp = Date.parse(new Date());
    renderTimePicker();
    $('.time').each(function () {
        var time_str = $(this).attr('time');
        var cur_time = new Date(time_str).getTime();
        var pro = parseInt($(this).next().text());
        if (cur_time <= timestamp && pro != 0) {
            $(this).parent().find('.info').html('进行中');
            $(this).parent().find('.info').addClass('in_progress_info')
        } else if(cur_time <= timestamp && pro == 0) {
            $(this).parent().find('.info').html('未开始')
            $(this).parent().find('.info').addClass('not_start_info')
        }
    })

    $('.time_exp_begin').each(function () {
        var flag = $(this).parent().parent().find("input[name='is_begin']").is(":checked")
        if (!flag) {
            var time_str = $(this).val();
            var begin_time = new Date(time_str).getTime();
            if (begin_time <= timestamp) {
                $(this).parent().parent().find('.info').html("没开始");
                $(this).parent().parent().find('.info').addClass('not_start_info');
            }
        }
    })

    $('.time_check').each(function () {
        var ms = 86400000
        var time_str = $(this).val();
        var deadline = new Date(time_str).getTime();
        var days = $(this).parent().parent().find("input[name='need_days']").val();
        if (days < 0) {
            var start_time = $(this).parent().parent().find('.timepicker').val()
            if (isTime(start_time)) {
                var myDate = new Date();
                cur_hour = parseInt(myDate.getHours());
                cur_min = parseInt(myDate.getMinutes());
                h_m = start_time.split(':');
                task_hour = parseInt(h_m[0]);
                task_min = parseInt(h_m[1]);
                if (task_hour < cur_hour || (task_hour == cur_hour && task_min < cur_min)) {
                    $(this).parent().parent().find('.info').html('SHOULD DO NOW');
                } else {
                   //
                }
            }
            $(this).parent().parent().find('.info').addClass('periodic_task_info');
        } else {
            deadline = deadline + (days-1) * ms;
            if (deadline <= timestamp) {
                var days = Math.floor((timestamp - deadline)/ms);
                if (days == 0) {
                    $(this).parent().parent().find('.info').html('DEADLINE TODAY');
                    $(this).parent().parent().find('.info').addClass('deadline_info');
                } else {
                    var str = '';
                    if (days > 1) {
                        str = days.toString() + ' DAYS';
                    } else {
                        str = days.toString() + ' DAY';
                    }
                    $(this).parent().parent().find('.info').html(str+" OVERDUE");
                    $(this).parent().parent().find('.info').addClass('not_start_info');
                }
            }
        }
    })

    $('.time_exp_end').each(function () {
        var flag = $(this).parent().parent().find("input[name='is_begin']").is(":checked")
        if (flag) {
            var time_str = $(this).val();
            var end_time = new Date(time_str).getTime();
            if (end_time <= timestamp) {
                $(this).parent().parent().find('.info').html("没完成");
                $(this).parent().parent().find('.info').addClass('deadline_info');
            }
        }
    })

    $("input[name='is_begin']:checked").each(function () {
        var deadline_ele = $(this).parent().parent().find("input[name='e_time']");
        flag = true;
        if (deadline_ele.hasClass('time_exp_end')) {
            var time_str = deadline_ele.val();
            var end_time = new Date(time_str).getTime();
            if (end_time <= timestamp) {
                flag = false;

            }
        }
        if (flag) {
            $(this).parent().parent().find('.info').html("进行中");
            $(this).parent().parent().find('.info').addClass('in_progress_info');
        }
    })

    $('.btn-add').click(function(){
		var str = $(this).parent().find('.add_content').html()
		$(this).parent().find('.add_line').append(str)
		renderAction();
		renderNum();
		renderChangeBtn();
		renderCancelBtn();
		renderDatePicker();
		renderTimePicker();
	})

	renderAction();
	renderNum();
	renderChangeBtn();
	renderCancelBtn();
	renderDatePicker();
})


function renderDatePicker() {
    $('.ipt_date').fdatepicker({
        format: 'yyyy-mm-dd'
    });
}


function renderChangeBtn() {
    $('.change_btn, .all_long_change_btn').off('click').click(function () {
        var pp = $(this).parent().parent();
        $(this).parent().parent().find('input, checkbox').removeAttr('disabled');
        $(this).parent().parent().find('.create_time').attr('disabled','disabled');
        $(this).hide();
        $(this).next().show();
        if(pp.find('a').length > 0){
            pp.find('a').hide();
            pp.find("input[name='content']").show();
            pp.find("input[name='content']").removeAttr('disabled');
        }
        if($(this).hasClass('all_long_change_btn')){
            pp.find('.change_btn').hide()
            pp.find('.cancel_btn').show()
        }
    })
}


function renderCancelBtn() {
    $('.cancel_btn, .all_long_cancel_btn').off('click').click(function () {
        var pp = $(this).parent().parent();
        $(this).parent().parent().find('input, checkbox').attr('disabled','disabled');
        $(this).hide();
        $(this).prev().show()
        if(pp.find('a').length > 0){
            pp.find('a').show();
            pp.find("input[name='content']").hide();
            pp.find("input[name='content']").attr('disabled','disabled').val('');
        }
    })
}


function renderAction() {
	$('.btn-del').off('click').click(function(){
		$(this).parent().parent().remove();
		renderNum();
	});

}


function renderNum() {
	$('table').each(function(index,e){
		$(this).find('tr .num').each(function(index2,e2){
		    $(this).html(index2+1)
        })
	})
}


function submitNew() {
    var flag = true;
    $('.ipt').each(function () {
        if(!$(this).is(":disabled") && $(this).val() == ''){
            flag = false;
        }
    })
    if (!flag) {
        alert('输入内容不能为空哦');
    }
    return flag;
}


function submitNewItem(str) {
    var flag = true;
    $("#"+str+" input[name='name']").each(function () {
        if($(this).val() == ''){
            flag=false;
        }
    })
    if (!flag) {
        alert('名称不能为空哦');
    }
    return flag;
}

function renderTimePicker() {
    $('input.timepicker').timepicker({
        timeFormat: 'HH:mm',
        interval: 30,
        minTime: '6',
        maxTime: '23',
        defaultTime: '',
        startTime: '6:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
}

function isTime(time_str){
   var regex=/^(?:(?:[0-2][0-3])|(?:[0-1][0-9])):[0-5][0-9]$/;
   return regex.test(time_str)
}