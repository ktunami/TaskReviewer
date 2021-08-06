$(function(){
    const timestamp = Date.parse(new Date());
    $('.time').each(function () {
        var time_str = $(this).attr('time');
        var cur_time = new Date(time_str).getTime();
        var pro = parseInt($(this).next().text());
        if (cur_time <= timestamp && pro != 0) {
            $(this).parent().addClass('bg_yellow');
        } else if(cur_time <= timestamp && pro == 0) {
            $(this).parent().addClass('bg_red');
        }
    })
	//新增行
	$('.btn-add1').click(function(){
		var str = $('#add_tpl').html();
		$('#add_body').append(str);
		renderAction();
		renderNum();
		renderSelect();
	})

    $('.btn-add2').click(function(){
		var str = $('#add_long_item').html();
		$('#add_long_item_line').append(str);
		renderAction();
		renderNum();
		renderChangeBtn();
		renderCancelBtn();
		renderDatePicker();
	})

	renderAction();
	renderSelect();
	renderNum();
	renderChangeBtn();
	renderCancelBtn();
	renderDatePicker();
})

function renderSelect() {
    $('.select').change(function () {
        if($(this).val() != 0){
            $(this).parent().next().find('.ipt').attr('disabled','disabled').val('');
        } else {
            $(this).parent().next().find('.ipt').removeAttr('disabled').val('');
        }
    })

}

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


//重新渲染删除
function renderAction() {
	$('.btn-del').off('click').click(function(){
		$(this).parent().parent().remove();
		renderNum();
	});

}
//重新渲染序号
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
    $("#"+str+" .add_long_item_line input[name='name']").each(function () {
        if($(this).val() == ''){
            flag=false;
        }
    })
    if (!flag) {
        alert('名称不能为空哦');
    }
    return flag;
}