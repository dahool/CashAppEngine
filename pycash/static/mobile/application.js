$(function() {
        // catch forms
/*    $(document).on("pageload", function() {
        $('a[data-cache=false]').on('click', function() {
            var $this = $(this);
            $.mobile.changePage($this.attr('href'),{reloadPage: true, transition: "fade"});
        });
        $('[form-submit]').on("click",function() {
            var frm = $(this).attr('form-submit');
            var rte = false;
            if ($(this).attr('return')) {
            	rte = $(this).attr('return');
            }
            doPostAction($(frm).attr('action'), $(frm).serialize(), frm, rte);
            return false;
        }); 
    });*/

    $( document ).bind( 'mobileinit', function(){
        $.mobile.loader.prototype.options.text = "Cargando...";
        $.mobile.loader.prototype.options.textVisible = true;
        $.mobile.loader.prototype.options.theme = "a";
        $.mobile.loader.prototype.options.html = "";
        $.mobile.page.prototype.options.domCache = true;
      });
    
    $(document).on("pageinit", function(){
        /*$('a[data-cache=false]').unbind('click').on('click', function() {
            var $this = $(this);
            var href = $this.attr('href');
            if (href == '#') {
                href = $.mobile.path.get();
            }
            $.mobile.changePage(href,{reloadPage: true, transition: "fade"});
        });*/
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

// force certain pages to be refreshed every time. mark such pages with
// 'data-cache="never"'
//
    jQuery(document).on('pagehide', 'div', function(event, ui) {
      
      var page = jQuery(event.target);
      
      if(page.attr('data-cache') == 'never'){
        page.remove();
      };
    });

// for pages marked with 'data-cache="never"' manually add a back button since
// JQM doesn't. this is *okay* because we know the browswer history stack is
// intact and goes to the correct 'back' location.
// specified back button - however!
//
/*
    jQuery('div').live('pagebeforecreate', function(event, ui){
      var page = jQuery(event.target);

      if(page.attr('data-cache') == 'never'){
        var header = page.find('[data-role="header"]');

        if(header.find('[data-rel="back"]').size() == 0){
          var back = jQuery('<a href="#" data-icon="back" data-rel="back">Back</a>');
          header.prepend(back);
        };
      };
    });*/
            
});

function resetHolder() {
    $this=$("#total-holder");
    $this.removeClass('ui-text-red');
    $this.html($this.attr('total-prefix')+$this.attr('total-value'));    
}

function summatory() {
    $("input[type=checkbox][summatory]").attr('checked',false);
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
           $holder.html($holder.attr('total-prefix')+total);
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
