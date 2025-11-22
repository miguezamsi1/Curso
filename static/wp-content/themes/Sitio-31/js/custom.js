(function ($) {
    "use strict";
    /* IGUALA ALTURA
     ================================================== */
    $.equalHeights = function (objeto, inner) {
        var tallest = 0;
        $(objeto).find(inner).each(function () {
            $(this).css({'height': 'auto'});
            if ($(this).outerHeight() > tallest) {
                tallest = $(this).outerHeight();
                console.log(tallest);
            }
        });
        $(objeto).find(inner).css({height: tallest + 'px'});
        return tallest;
    };

    /* MUESTRA - OCULTA BUSCADOR
     ================================================== */
    $.openSearch = function () {
        if ($('.form-type-textfield').hasClass('active')) {
            $(".form-type-textfield").hide().removeClass("active");
        } else {
            $(".form-type-textfield").show().addClass("active");
            $("#form-searchf").focus();
        }
    };
    $.outSearch = function () {
        $(".form-type-textfield").hide().removeClass("active");
    };

    /* CALCULO DE ANCHO DE CAROUSEL INDICATORS LI
     ================================================== */
    $.indicatorWidth = function () {
        var cont = 1;
        $("#main .carousel-indicators").each(function () {
            $(this).addClass("indicator-" + cont);
            $("#main .indicator-" + cont + " li").width(Math.floor(($(this).outerWidth() - (14 * ($("#main .indicator-" + cont + " li").length - 1))) / $("#main .indicator-" + cont + " li").length));
            cont = cont + 1;
        });
    };

    $.search = function () {
        var searchBlock = $("#block-search-form a");
        searchBlock.on({
            click: function () {
                $.openSearch();
            },
            keypress: function () {
                if (event.which === 13) {
                    $.openSearch();
                    $("#form-searchf").focus();
                }
                if (event.which === 27) {
                    $.outSearch();
                }
            }
        });
        $("#form-searchf").on("mouseleave", function () {
            $.outSearch();
        });
    };

    /* CALCULO VIEWPORT WIDTH
     ================================================== */
    $.overviewWidth = function () {
        var viewport = parseInt($("#programas-items .viewport").css('width'));
        var margin = parseInt($("#programas-items .overview li").css('margin-right'));
        console.log("margin: " + margin);
        var marginTotal = 0;
        var elements = 0;

        var liMinWidth = 106;
        var liWidth = liMinWidth;


        elements = Math.floor(viewport / liMinWidth);
        marginTotal = (elements - 1) * margin;


        if ((viewport - marginTotal) % liMinWidth <= liMinWidth) {
            liWidth = Math.ceil((viewport - marginTotal) / elements);
            $("#programas-items .overview li").css({
                'width': liWidth
            });
        }
//        console.log((viewport - marginTotal) % liMinWidth <= liMinWidth);
//        console.log(Math.ceil((viewport - marginTotal) / elements));
//        console.log(liWidth);

        /*        $('#programas-items').tinycarousel({
         infinite: false,
         animationTime: 300
         });*/
    };


    /* Hero height
     ================================================== */
    $.hero = function () {
        var windowHeight = $(window).height();
        var headerHeight = $("header#head").outerHeight();
        var footerHeight = $("footer#footer-bot").outerHeight();
        var wpadminHeight = $("#wpadminbar").outerHeight();
        if ($(window).width() > 768) {
            $('.hero').css({'min-height': (windowHeight - headerHeight - footerHeight - wpadminHeight)});
        } else {
            $('.hero').css({'min-height': 'auto'});
        }
    };


    /* MAIN WIDTHS, HEIGHTS & POSITIONS
     ================================================== */
    $.main = function () {
        $.search();

        $(".carousel").each(function () {
            $(this).carousel();
        });
        $('#main-carousel').carousel({
            interval: 400,
            wrap: false
        });
        $('#alertas').carousel({
            interval: 90000,
            wrap: false
        });

        //$('#videos-carousel').carousel('pause');
        $('#videos-carousel').on('slide.bs.carousel', function () {
            console.log("CHANGE VIDEO" + player1.stopVideo());
            //player1.stopVideo();
            //player2.stopVideo();
            //jQuery('#videos-carousel').carousel('pause');

            document.getElementById('player1').contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*');
            document.getElementById('player2').contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*');
        });

        function onPlayerStateChange() {
            console.log('PLAYER CHANGE');
        }

        if ($(window).width() > 768) {
            $("#bg-header").height($("header#head .container-fluid").height());
            $("footer#footer-bot").css({'height': 'auto'});
            $("header#head").css({'height': 'auto'});
            var headerHeight = $("header#head").height();
            var footerHeight = $("footer#footer-bot").outerHeight();
            var windowHeight = $(window).height();

            var noticiasHeight = $("#noticias img").height();

            $("#noticias .text").css({'height': noticiasHeight + 'px'});

            var bloqueHeight = $("#videos-carousel").parent().height() + 2;
            $("#banner").outerHeight(bloqueHeight);

            $(".ref").css({'height': '100%'});
            var itemHeight = ($("#contacto-gob").outerHeight() + $("#videos").outerHeight() + 15) - 80 - $("#programas").height();
            $("#main-carousel .item").height(itemHeight);

            $(".control").css({'margin-top': headerHeight + 'px'});
            var mainHeight = windowHeight - headerHeight - footerHeight;

            var newsScroll = $("#destacados .panel");
            $("#news .scroll").height((newsScroll.height()) + 20);


            $("#servicios .tab-content").css({'height': $("#servicios .nav-tabs").height()});
            $.equalHeights($("footer#footer-bot .top"), $("footer#footer-bot .top a"));

            if (mainHeight < 470) {
                $("#main .container-fluid").css({'min-height': mainHeight});
            }

            $("#programas-items").on({
                mouseenter: function () {
                    $("#programas-items .buttons").css({'opacity': 1});
                },
                mouseleave: function () {
                    $("#programas-items .buttons").css({'opacity': 0});
                }
            });

//                $("#wpadminbar").length < 1 ? main = windowHeight - headerHeight - footerHeight : main = windowHeight - headerHeight - footerHeight - 86;
//                $("#main .container-fluid").innerHeight(main);
        } else if ($(window).width() <= 500) {
            $("#main").css({height: 100 + "%"});


            // Scroll
            //$('[data-scrollable]').niceScroll({cursorborder: 0, cursorcolor: "#00deff"});
            //$('[data-scrollable]').getNiceScroll().resize();
            $('#menu ul.collapse').on('shown.bs.collapse', function (e) {
                //$('#menu').getNiceScroll().resize();
            });

            // Collapse
            $('#menu ul.collapse').on('show.bs.collapse', function (e) {
                e.stopPropagation();
                var parents = $(this).parents('ul:first').find('> li.open [data-toggle="collapse"]');
                if (parents.length) {
                    parents.trigger('click');
                }
                $(this).parent().addClass("open");
            });

            $('#menu ul.collapse').on('hidden.bs.collapse', function (e) {
                e.stopPropagation();
                $(this).parent().removeClass("open");
            });
        }

    };

    $(window).load(function () {
        if ($("#main.institucion .imagen").length) {
            if (window.innerWidth > 1000) {
                $("#main.institucion .social").wrapInner("<div class='inner'></div>");
                $("#main.institucion .social").css({'height': $("#main.institucion .imagen").height()});

            } else {
                $("#main.institucion .social").css({'padding-top': '0px'});
            }
            $("#main.institucion .scroll").css({'height': $("#main.institucion .imagen").height()});
        } else {
            if (window.innerWidth > 1000) {
                $("#main.institucion .social").css({'padding-top': '80px'});
            } else {
                $("#main.institucion .social").css({'padding-top': '0px'});
            }
        }



        /* CONTROL PAUSE - PLAY
         ================================================== */
        $('#control').on({
            click: function () {
                if ($(this).children().hasClass('fa-pause')) {
                    $('#main-carousel').carousel('pause');
                    $(this).children().removeClass('fa-pause').addClass('fa-play');
                } else {
                    $('#main-carousel').carousel('cycle');
                    $(this).children().removeClass('fa-play').addClass('fa-pause');
                }
            },
            keypress: function () {
                if (event.which === 13) {
                    click();
                }
            }
        });


        /* Hero height
         ================================================== */
        var windowHeight = $(window).height();
        $('.hero').height(windowHeight);

        $.main();

        $.overviewWidth();


    });
    $(document).ready(function () {
        /*ALERTAS */
        /*$.equalHeights($("#alertas"), $("#alertas [class*='col-']"));
        $.equalHeights($("#pasarela"), $("#pasarela [class*='col-']"));
        $.equalHeights($("#main.servicios #servicios"), $("#main.servicios #servicios [class*='col-']:not(.col-xs-0)"));

        $("#alertas-next").outerHeight($("#alertas .carousel-inner").height());*/
        console.log("ALTO ALERTA :: " + $("#alertas .carousel-inner").height());
        /* Mobile o desktop */
        var md = new MobileDetect(window.navigator.userAgent);
        console.log(md.mobile());
        /*console.log("mobile " + jQuery.browser.mobile);*/
        if (md.mobile()) {
            $(".vermobile").each(function () {
                $(this).css({'display': 'block'});
            });
            if (document.getElementById('postcontent')) {
                $("div#postcontent").removeClass("scroll");
            }
            if (document.getElementById('contenido-comunica')) {
                $("div#contenido-comunica").removeClass("scroll");
                $("div#contenido-comunica").removeClass("altura");
            }
            if (document.getElementById('contenido-search')) {
                $("div#contenido-search").removeClass("scroll");
                $("div#contenido-search").removeClass("altura");
            }
            
            if (document.getElementById('agendapresi')) {
                $("div#agendapresi").removeClass("scroll");
                $("div#agendapresi").removeClass("altura");
            }
            
        } else {
            $(".verdesktop").each(function () {
                $(this).css({'display': 'block'});
            });
        }


        $("#programas .crsl-programas a").wrap("<div class='crsl-item'></div>");
        $("#programas-segunda .crsl-programas-segunda a").wrap("<div class='crsl-item'></div>");

        $('.scroll ul a').on('click', function (e) {
            if ($('.scroll ul a.active').length) {
                //$('.scroll').getNiceScroll().resize();
            }
        });

        //$("body").niceScroll();


        $('#menu ul.collapse').on('hidden.bs.collapse', function (e) {
            e.stopPropagation();
            $(this).parent().removeClass("open");
        });


        $('[data-toggle="tooltip"]').tooltip({html: true});
        $("#menu .dropdown-toggle").append('<span class="fa fa-angle-right"></span>');

        $("#menu li.dropdown-submenu a").on({
            mouseenter: function () {
                $(this).parent().find("> .dropdown-menu").addClass('open');
            },
            mouseleave: function () {
                $(this).parent().find(".dropdown-menu").removeClass('open');
            },
            focus: function () {
                $(this).parent().find(".dropdown-menu").addClass('open');
            }
        });
        $('.crsl-programas').responsiveCarousel({
            visible: 5,
            itemMinWidth: 106,
            itemMargin: 2,
            itemEqualHeight: true
        });
        $('.crsl-programas-segunda').responsiveCarousel({
            visible: 5,
            itemMinWidth: 106,
            itemMargin: 2,
            itemEqualHeight: true
        });
        $.indicatorWidth();
        /*        $(".scroll").niceScroll();
         $(".scroll").getNiceScroll().resize();
         */
        $('.scroll').css({overflow: 'auto'});
        /* SIDEBAR CONTROL
         ================================================== */
        var toggleBtn = $('[data-toggle="sidebar-menu"], .sidebar .close');
        // If No Sidebar Exit
        if (!toggleBtn.length)
            return false;
        toggleBtn.on({
            click: function () {
                $('body').toggleClass('show-sidebar');
                $.indicatorWidth();

                /* SIDEBAR CONTROL
                 ================================================== */
                if ($(".sidebar.left").length) {
                    $(".sidebar.left").toggleClass('hide');
                }
            },
            keypress: function () {
                if (event.which === 13) {
                    $('body').toggleClass('show-sidebar');
                    $.indicatorWidth();
                    //$('#menu').getNiceScroll().resize();
                }
            }
        });
        $('.img-swap').hover(function (){

            console.log($(this).data('img1'));
            $(this).attr("src",$(this).data('img1'))
        },function(){
            console.log($(this).data('img2'));
            $(this).attr("src",$(this).data('img2'))
        });


    });
    $(window).resize(function () {
        var windowHeight = $(window).height();
        $('.hero').height(windowHeight);
        $("header#head .container-fluid").height("100%");
        $.equalHeights($("#footer-bot .top"), $("footer#footer-bot .top a"));
        $.indicatorWidth();
        $.main();
        $.overviewWidth();
        $.search();
    });
    $('#main').on('click', function () {
        $(".sidebar.left").addClass('hide');
        $('body').removeClass('show-sidebar');
        $.indicatorWidth();
    });
    var KEYCODE_ESC = 27;
    $(document).keyup(function (e) {
        if (e.keyCode === KEYCODE_ESC) {
            $(".sidebar.left").addClass('hide');
            $('body').removeClass('show-sidebar');
            $("#menu li").removeClass('open');
            $.indicatorWidth();
        }
    });
})(jQuery);


(function (a) {
    (jQuery.browser = jQuery.browser || {}).mobile = /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))
})(navigator.userAgent || navigator.vendor || window.opera);