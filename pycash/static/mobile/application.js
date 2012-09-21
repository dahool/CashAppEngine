$(function() {
    $( document ).bind( 'mobileinit', function(){
        $.mobile.loader.prototype.options.text = "Cargando...";
        $.mobile.loader.prototype.options.textVisible = true;
        $.mobile.loader.prototype.options.theme = "a";
        $.mobile.loader.prototype.options.html = "";
        $.mobile.page.prototype.options.domCache = true;
        $.mobile.transitionFallbacks.slideout = "none";
        //$.mobile.selectmenu.prototype.options.nativeMenu = false;
      });
    
    $(document).on("pageinit", function(){
        $('[form-submit]').unbind('click').on("click",function() {
            var frm = $(this).attr('form-submit');
            var rte = false;
            if ($(this).attr('return')) {
            	rte = $(this).attr('return');
            }
            doPostAction($(frm).attr('action'), $(frm).serialize(), frm, rte);
            return false;
        });
        $("[data-role=header]").fixedtoolbar({ tapToggle: false });
    });     
    
    $(document).on("dateboxbeforecreate", function() {
        $.mobile.datebox.prototype.options.lang = 'es';
        $.mobile.datebox.prototype.options.disableManualInput = true;
    })
    
    $(document).on("pageshow", function(){
        $("[field-focus=true]").focus();
        $("[field-clear=true]").val("");
        $("[reset-form=true]").find('input,select').each(function() {
            if ($(this).is("select")) $(this).val(-1);
            else if ($(this).is("[type=radio]")) {
                $(this).attr('checked',false);
                $(this).removeClass('ui-btn-active');
            }
            else $(this).val("");
        });
        summatory();
    });

   // initDatebox();
// force certain pages to be refreshed every time. mark such pages with
// 'data-cache="never"'
//
    jQuery(document).on('pagehide', 'div', function(event, ui) {
      var page = jQuery(event.target);
      if(page.attr('data-cache') == 'never'){
        page.remove();
      };
    });
            
});

function resetHolder() {
    $("input[type=checkbox][summatory]").attr('checked',false);
    $this=$("#total-holder");
    $this.removeClass('ui-text-red');
    $this.html($this.attr('total-prefix')+$this.attr('total-value'));
    $("div.ui-checkbox").find('.ui-icon-checkbox-on').addClass('ui-icon-checkbox-off').removeClass('ui-icon-checkbox-on');
    $("div.ui-checkbox").find('.ui-checkbox-on').addClass('ui-checkbox-off').removeClass('ui-checkbox-on');    
}

function summatory() {
    resetHolder();
    $("input[type=checkbox][summatory]:visible").on('change', function() {
       var total = 0;
       var $holder = $("#total-holder");
       $("input[type=checkbox][summatory]:checked").each(function() {
           total = total + parseFloat($(this).attr('summatory'));
       });
       if (total == 0) {
           resetHolder();
       } else {
           if (!$holder.hasClass('ui-text-red')) $holder.addClass('ui-text-red');
           $holder.html($holder.attr('total-prefix')+total.toFixed(2));
       }
    });
    $("#total-holder").on('click', function() {
        resetHolder();
    });
} 

function doPostAction(url, data, elem, rte) {
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        beforeSend: function(r,s) {
            $.mobile.showPageLoadingMsg();
        },
        complete: function(r,s) {
            $.mobile.hidePageLoadingMsg();
        },
        success: function(data) {
        	if (data.success) {
            	if (data.msg) {
                    $(elem).notify({'msg': data.msg,
                        'type': 'success',
                        'onClose': function() {
                            afterSubmit(elem, rte);
                        }});            	    
            	    /*
                    $(elem).simpledialog({
                        'mode' : 'bool',
                        'prompt' : data.msg,
                        'useModal': true,
                        'buttons' : {
                          'OK': {
                            click: function() {
                            	afterSubmit(elem, rte);
                            }
                        }
                    }
                    });*/
            	}  else {
                    afterSubmit(elem, rte);
                }
        	} else {
        	    if (data.msg) {
        	        $(elem).notify({'msg': data.msg,
        	                        'type': 'error',
        	                        'onClose': function() {
        	                            $("[field-focus=true]").focus();
        	                        }});
        	    }
            	/*if (data.msg) {
                    $(elem).simpledialog({
                        'mode' : 'bool',
                        'prompt' : data.msg,
                        'useModal': true,
                        'buttons' : {
                          'OK': {
                            click: function() {
                            	$("[field-focus=true]").focus();
                    		}
                            }
                        }
                    });
            	} */       		
        	}
        },
        dataType: "json"
    });
}

function showError(msg) {
    $("#notify").html(msg).notify('show');
}

function afterSubmit(elem, rte) {
    if ($(elem).attr('after-submit-clean')) {
        var values = $(elem).attr('after-submit-clean')
        if ('form' == values) {
            $(elem).find('input,select').each(function() {
                $(this).val("");
            });                
        } else {
            values = values.split(",");
            $.each(values, function(idx, value) {
                $("#"+value).val("");
            });
            $("#"+values[0]).focus();                
        }
    }    
    if (rte) {
        if (rte == 'back') {
            window.history.back();
        } else {
            $.mobile.changePage(rte, {reloadPage: true});
        }
    }
}

function confirmSingleAction(url, id) {
	var $elem = $('div[data-role="content"]:visible');
	var rte = $elem.attr("data-return");
    $elem.simpledialog({
        'mode' : 'bool',
        'prompt' : "¿Confirma eliminación?",
        'useModal': true,
        'buttons' : {
          'Si': {
            click: function() {
            	doPostAction(url, {"id": id}, $elem, rte);
            },
    		icon: "delete",
    		theme: "c"
          },
    	  'No': {
    		click: function() {
    	    },
    	  }
        }
    });	
}
/*
function initDatebox() {
    $("input[data-role=datebox]").each(function() {
        $(this).scroller({preset: 'date', theme: 'jqm', mode: 'scroller', lang: 'es'});
        $(this).attr("readonly", true);
    });
    $("input[data-role=datebox]").on('click', function() {
        $(this).scroller('show');
    });    
}*/