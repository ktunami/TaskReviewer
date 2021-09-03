$(function(){
    const timestamp = new Date(new Date().toLocaleDateString()).getTime();
    var ms = 86400000
    renderTimePicker();
    renderAutoTextarea();
    $('.time').each(function () {
        var time_str = $(this).attr('time');
        var cur_time = new Date(dateFormatChange(time_str)).getTime();
        var pro = parseInt($(this).next().text());
        if (cur_time <= timestamp && pro != 0) {
            $(this).parent().find('.info').html('IN PROGRESS');
            $(this).parent().find('.info').addClass('in_progress_info')
        } else if(cur_time <= timestamp && pro == 0) {
            $(this).parent().find('.info').html('NOT STARTED')
            $(this).parent().find('.info').addClass('not_start_info')
        }
    })

    $('.time_exp_begin').each(function () {
        var flag = $(this).parent().parent().find("input[name='is_begin']").is(":checked")
        if (!flag) {
            var time_str = $(this).val();
            var begin_time = new Date(dateFormatChange(time_str)).getTime();
            if (begin_time <= timestamp) {
                $(this).parent().parent().find('.info').html("NOT STARTED");
                $(this).parent().parent().find('.info').addClass('not_start_info');
            }
        }
    })

    $('.time_check').each(function () {
        var time_str = $(this).val();
        var deadline = new Date(dateFormatChange(time_str)).getTime();
        var days = $(this).parent().parent().find("input[name='need_days']").val();
        if (days < 0) {
            var start_time = $(this).parent().parent().find("input[name='start_time']").val()
            var end_time = $(this).parent().parent().find("input[name='end_time']").val()
            if (isTime(start_time)) {
                if (isLaterThanNow(start_time)) {
                    $(this).parent().parent().find('.info').html('DO IT NOW');
                }
            }
            if (isTime(end_time)) {
                if (isLaterThanNow(end_time)) {
                    $(this).parent().parent().find('.info').html('==OVERDUE==');
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
            } else {
                var days = Math.floor((deadline - timestamp)/ms);
                $(this).parent().parent().find('.info').html('D DAY '+days);
            }
        }
    })

    $('.time_exp_end').each(function () {
        var flag = $(this).parent().parent().find("input[name='is_begin']").is(":checked")
        if (flag) {
            var time_str = $(this).val();
            var end_time = new Date(dateFormatChange(time_str)).getTime();
            if (end_time <= timestamp) {
                $(this).parent().parent().find('.info').html("UNFINISHED");
                $(this).parent().parent().find('.info').addClass('deadline_info');
            }
        }
    })

    $("input[name='is_begin']:checked").each(function () {
        var deadline_ele = $(this).parent().parent().find("input[name='e_time']");
        flag = true;
        if (deadline_ele.hasClass('time_exp_end')) {
            var time_str = deadline_ele.val();
            var end_time = new Date(dateFormatChange(time_str)).getTime();
            if (end_time <= timestamp) {
                flag = false;
            }
        }
        if (flag) {
            var days = Math.floor((end_time - timestamp)/ms);
            $(this).parent().parent().find('.info').html('D DAY '+days);
            $(this).parent().parent().find('.info').addClass('in_progress_info');
        }
    })

    $('.delete_btn').click(function () {
        if(confirm("确定要删吗？兄弟")) {
            window.location.href=$(this).data('href')
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
		renderMouseOver();
		renderSelectChange();
	})

	renderAction();
	renderNum();
	renderChangeBtn();
	renderCancelBtn();
	renderDatePicker();
	renderMouseOver();
	renderSelectChange();
})


function renderDatePicker() {
    $('.ipt_date').fdatepicker({
        format: 'yyyy-mm-dd'
    });
}

function renderChangeBtn() {
    $('.change_btn, .all_long_change_btn').off('click').click(function () {
        var pp = $(this).parent().parent();
        $(this).parent().parent().find('input, checkbox, textarea, select').removeAttr('disabled');
        $(this).hide();
        $(this).next().show();
        $(this).next().next().show();
        $(this).next().next().next().show();
        pp.find('.tip-add').show();
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
        $(this).parent().parent().find('input, checkbox, textarea, select').attr('disabled','disabled');
        $(this).hide();
        $(this).prev().show()
        $(this).next().hide()
        $(this).next().next().hide()
        pp.find('.tip-add').hide();
        if(pp.find('a').length > 0){
            pp.find('a').show();
            pp.find("input[name='content']").hide();
           // pp.find("input[name='content']").attr('disabled','disabled').val('');
        }
    })
}

function submit_tip_change(form_id) {
    $('#'+form_id).submit();
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

function submitCheck(str) {
    var flag = true;
    var flag_money = true;
    $("#"+str+" input[name='money']").each(function () {
        if ($(this).val() == '') {
            flag = false;
        }
    })

    $("#"+str+" select").each(function (){
       if ($(this).find("option:selected").val()=='') {
            flag = false;
        }
    })

    $("#"+str+" input[name='money']").each(function (){
        if (isNaN($(this).val())) {
            flag_money = false;
        }
    })
    if (!flag) {
        alert("每一项都不能为空")
    }
    if (!flag_money) {
        alert("金额必须是数字")
    }
    return flag && flag_money;
}


function submitNewItem(str) {
    var flag1 = true;
    var flag2 = true;
    var flag3 = true;
    $("#"+str+" input[name='name']").each(function () {
        if($(this).val() == '') {
            flag1 = false;
        }
    })
    var regex = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/;
    $("#"+str+" .must_link").each(function () {
        if($(this).val() != '' && !regex.test($(this).val())) {
            flag2 = false;
        }
    })
    $("#"+str+" input[name='is_begin']").each(function () {
        if($(this).is(':checked')) {
            var tr = $(this).parent().parent();
            if (tr.find("input[name='s_time']").val()=='' || tr.find("input[name='e_time']").val()=='') {
                flag3 = false;
            }
        }
    })

    if (!flag1) {
        alert('名称不能为空哦');
    }
    if (!flag2) {
        alert('输入的"链接"不是正经URL');
    }
    if (!flag3) {
        alert('已开始的项目必须设置起止日期');
    }
    return flag1 && flag2 && flag3;
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

function dateFormatChange(date_str) {
    return date_str.split('-').join('/')
}

function renderMouseOver(){
    $('.high_line').mouseenter(function () {
        $(this).addClass('highlight_border')
    })
    $('.high_line').mouseleave(function () {
        $(this).removeClass('highlight_border')
    })
}

function renderSelectChange(){
    str = $('#shopping_categories').val()
    dic = JSON.parse(str)
    $('.main_category').each(function (){
        $(this).change(function (){
            cur_key = $(this).find("option:selected").val();
            if (cur_key != '') {
                arr = dic[cur_key]
                html_str = '';
                for (i=0; i < arr.length; ++i){
                    html_str += "<option value='"+arr[i]+"'>"+arr[i]+"</option>"
                }
                $(this).parent().parent().find('.sub_select').html(html_str)
            } else {
                $(this).parent().parent().find('.sub_select').html('')
            }
        })
    })
}

function renderAutoTextarea() {
    $.fn.autoHeight = function(){
        function autoHeight(elem){
            elem.style.height = 'auto';
            elem.scrollTop = 0; //防抖动
            elem.style.height = elem.scrollHeight + 'px';
        }
        this.each(function(){
            autoHeight(this);
            $(this).on('keyup', function(){
                autoHeight(this);
            });
        });
    }
    $('textarea[autoHeight]').autoHeight();
}

function isLaterThanNow(time) {
    var curDate = new Date();
    cur_hour = parseInt(curDate.getHours());
    cur_min = parseInt(curDate.getMinutes());
    h_m = time.split(':');
    task_hour = parseInt(h_m[0]);
    task_min = parseInt(h_m[1]);
    if (task_hour < cur_hour || (task_hour == cur_hour && task_min < cur_min)) {
        return true;
    } else {
        return false;
    }
}


function getSetList(arr) {
    var arrry= [arr[0]];
    for (var i = 1; i < arr.length; i++) {
        if (arr[i] !== arr[i-1]) {
            arrry.push(arr[i]);
        }
    }
    return arrry;
}

$(document).ready(function() {
    var str = $('#st_json').val();
    if (str != '') {
        var dic = JSON.parse(str);
        var cate = new Array();
        var month = new Array();
        var money = new Array();
        for (i=0; i<dic.length; ++i) {
            var m = dic[i]['create_date']['qyear'] + "-" + dic[i]['create_date']['month']
            month.push(m)
            cate.push(dic[i]['category'])
            money.push(dic[i]['money'])
        }
        cate_type = getSetList(cate);
        month_type = getSetList(month);
        datas = {};
        var series =  [];
        for (i = 0; i < cate_type.length; ++i) {
            datas[cate_type[i]] = {};
        }
        for (i = 0; i < month.length; ++i) {
            datas[cate[i]][month[i]] = money[i];
        }
        for (key in datas) {
            ele = {};
            ele['name'] = key;
            ele['data'] = new Array();
            for (i = 0; i < month_type.length; ++i) {
                if (datas[key].hasOwnProperty(month_type[i])) {
                    ele['data'].push(datas[key][month_type[i]])
                } else {
                    ele['data'].push(0)
                }
            }
            series.push(ele);
        }
        console.log(series)
        var title = {
            text: '每月支出'
        };
        var subtitle = {
            text: '来源: 额的血汗钱'
        };
        var xAxis = {
            categories: month_type
        };
        var yAxis = {
        title: {
            text: '人民币 (单位：元)'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
        };

        var tooltip = {
            valueSuffix: '元'
        }

        var legend = {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        };

        var json = {};

        json.title = title;
        json.subtitle = subtitle;
        json.xAxis = xAxis;
        json.yAxis = yAxis;
        json.tooltip = tooltip;
        json.legend = legend;
        json.series = series;

        $('#container').highcharts(json);
    }
});