// @2017/07/05
$(function(){

      var api_domain = $("#api_domain").val();
      var access_token = $("#access_token").val();
      var club_id = $("#club_id").val();
      var league_id = $("#league_id").val();
      var title;
      var billing_code;
      function getCartPro(pageNum) {
          var limit = 20;//初始化值
          $.ajax({
            type: "GET",
            url: api_domain+"/api/clubs/"+ club_id +"/cart/items?page="+pageNum+"&limit="+limit,
            headers: {"Authorization": "Bearer "+ access_token +""},
            dataType: "json",
            contentType: 'application/json',
            success: function(data, status, xhr) {
                  console.log(data);
              var pageData = data.rs.data;
              var inner_html = "";

              for (var i in pageData) {
                  inner_html += '<li class="collection-item avatar list-item-info">';
                  inner_html += '<img src="'+ pageData[i].img +'" alt="" class="circle" style="border-radius:0;">';
                  inner_html += '<span class="title" data_pro_id="'+pageData[i].item_id+'">'+pageData[i].title+'</span>';
                  inner_html += '<p>品牌: '+pageData[i].brand_title+'</p>';
                  inner_html += '<p>规格: '+pageData[i].spec_title+'</p>';
                  inner_html += '<div class="hilight flex-separate">';
                  inner_html += '<input type="hidden" value="'+ pageData[i].spec_id +'" class="spec_template">';
                  inner_html += '<span class="one-price">'+pageData[i].amount/100+'元/'+pageData[i].unit+'</span>';
                  inner_html += '<div class="qunatity" style="padding-right: 2rem;">数量:';
                  inner_html += '<span class="one-quantity" style="margin-left: 1rem;">'+pageData[i].quantity+'</span>';
                  inner_html += '</div></div></li>';
                };
                $('#list-item').append(inner_html);

                // watch input change
                // $(document).on("input",".J_input",function(){
                //     getTotal();
                // });


                // 计算总金额
                var coupons_fee = 0;

                // 优惠券的使用
                $('#coupons-s').on('click',function(){
                  var code = $('#coupons-code').val();
                  $.ajax({
                    type: "GET",
                    url: api_domain+"/api/clubs/"+ club_id +"/coupons/codes/"+code,
                    headers: {"Authorization": "Bearer  {{access_token}}"},
                    contentType: 'application/json',
                    dataType:'json',
                    success: function(data, status, xhr) {
                        // console.log(data);
                        if(data.err_code == 200){
                            $('#coup-code').val(data.rs._id);
                            $('#coupon_fee').val(parseFloat(data.rs.amount)/100);
                            $('#coupons-fee').show().css({'display': 'flex'});
                            $('#coupons-fee span').css({'color':'green'}).html('此优惠券:&nbsp&nbsp&nbsp&nbsp&nbsp¥&nbsp'+parseFloat(data.rs.amount)/100+'元');
                            $('#filled-in-box').next().show();

                            $("input[type='checkbox']").on('change',function(){
                              console.log($(this).prop('checked'));
                              if($(this).prop("checked")==true){
                                coupons_fee = parseFloat(data.rs.amount)/100;
                                getTotal();
                              }else if($(this).prop("checked")==false){
                                coupons_fee = 0;
                                getTotal();
                              }
                              // var check_val = [];
                              //     for(k in obj){
                              //       if(obj[k].checked)
                              //          check_val.push(obj[k].value);
                              //     }
                            })

                        }else if(data.err_code == 403){
                            $('#coupons-fee').show().css({'display': 'flex'});
                            $('#coupons-fee span').css({'color':'red'}).html('此优惠券已被使用');
                            $('#filled-in-box').next().hide();
                        }else if(data.err_code == 408){
                            $('#coupons-fee').show().css({'display': 'flex'});
                            $('#coupons-fee span').css({'color':'red'}).html('此优惠券已超过有效期');
                            $('#filled-in-box').next().hide();
                        };
                    }
                  })
                });

                function getTotal(){
                  var num = $(".list-item-info").length;
                  var total_price=0;
                  var express_fee = 0;

                  for(var i=0;i<num;i++){
                    var one_price = $(".list-item-info").eq(i).find(".one-price").text();
                    // console.log(one_price);
                    var quantity = $(".list-item-info").eq(i).find(".one-quantity").text();
                    // console.log(quantity);
                    var one_total = parseFloat(one_price)*quantity;
                        total_price += parseFloat(one_total);
                  }
                    // $(".footer-total-price").children().html(total_price.toFixed(2));
                    $("#pro-fee").text(total_price.toFixed(2));

                      // 获取运费分类段位
                    $.ajax({

                        type: "GET",
                        url: api_domain+"/api/def/leagues/"+ league_id +"/shipping-costs",
                        headers: {"Authorization": "Bearer "+ access_token +""},
                        contentType: 'application/json',
                        success: function(data, status, xhr) {
                          var data_obj = JSON.parse(data);
                          if( data_obj.err_code == '200'){
                            var dataObj = data_obj.rs;
                            for(var j=0; j<dataObj.length;j++){
                              if(total_price >=dataObj[j]['_min'] && total_price < dataObj[j]['_max']){
                                express_fee = dataObj[j].cost;
                              }
                              else{
                                console.log('error');
                              }
                            }
                          }
                          $("#express-fee").text(express_fee.toFixed(2));
                          $("#shipping_cost").val(express_fee.toFixed(2));
                          $("#footer-bar span").text((total_price+express_fee-coupons_fee).toFixed(2));
                          $("#total_amount").val((total_price).toFixed(2));
                        }
                    });

                };

                getTotal();

                // 组织json数据
                var items = [];
                $('.list-item-info').each(function(index) {
                  var item_id = $(".title",$(this)).attr("data_pro_id");
                  var spec_id =  $(".spec_template",$(this)).val();
                  var quantity = $(".one-quantity",$(this)).text();
                  obj =  {"item_id":item_id,"spec_id":spec_id,"quantity":quantity};
                  items.push(obj);
                 });
                 $("#item_input").val(JSON.stringify(items))

                // 收货地址和发票信息
               var address = {};
               var billing_addr = {};

                // 下单操作
                $("#sub-order").on('click',function(event){
                  var name = $("#name").val();
                  var phone = $("#phone").val();
                  var addr = $("#addr").val();
                  var coupon_id = $("#coup-code").val();
                  var coupon = {"datas":[{"_id":coupon_id}]};
                  console.log(JSON.stringify(coupon));

                  // 发票信息
                  // console.log($('#test1').attr('checked'));
                      title = $("#title").val();
                      billing_code = $("#billing_code").val();
                  address = {"name":name,"phone":phone,"_addr":addr};
                  billing_addr = {'tfn':billing_code,'company_title':title}
                  $("#addr_input").val(JSON.stringify(address));
                  $("#billing_addr_input").val(JSON.stringify(billing_addr));
                  $("#coupon_input").val(JSON.stringify(coupon));
                  if(items.length == 0){
                    $.alert('您还没有选择任何商品!')
                     event.preventDefault();
                  }else if(name == '' || phone == '' || addr == ''){
                    $.alert("请填写收货地址!");
                    event.preventDefault();
                  }else if($('#test1').prop('checked') == true){
                    if( title == '' || billing_code == ''){
                      $.alert('发票信息填写不完整!')
                       event.preventDefault();
                    }else{
                      $(".order-form").submit();
                    }
                  }else{
                    $(".order-form").submit();
                  }

                });

              }
            })
      };
      getCartPro('1');
      getBilling();
      // 发票信息
      $("#modal2").modal();
      function getBilling(){
        $.ajax({
          type: "GET",
          url: api_domain+ "/api/addr/billings",
          headers: {"Authorization": "Bearer "+access_token+""},
          contentType: 'application/json',
          success: function(data, status, xhr) {
                console.log(data);
                data_obj = JSON.parse(data);
              var pageData = data_obj.rs;
              var _html = "";
              var modal2_html = '';
              if(pageData == ''){
                  $('#row').append('<div class="billing-wrap" style="margin-top:4rem;border-top:1px solid #9e9e9e;padding-top: 1.5rem; display:none;">'
                      + '<div class="input-field">'
                      + '<input id="title" type="text" style="font-size:16px;" class="validate">'
                      +  '<label for="title" class="active" style="font-size:14px;">公司抬头:</label>'
                      + '</div>'
                      + '<div class="input-field">'
                      +  '<input id="billing_code" type="number" style="font-size:16px;" class="validate">'
                      +  '<label for="billing_code" class="active" style="font-size:14px;">公司税号:</label>'
                      + '</div>'
                      +'</div>');
              }
              else{
                  _html += '<div class="billing-wrap" style="margin-top:4rem;border-top:1px solid #9e9e9e;padding-top: 1.5rem; display:none;">';
                  _html +=  '<div class="input-field">';
                  _html += '<input id="title" type="text" class="validate" style="font-size:16px;" value="'+ pageData[0].company_title +'">';
                  _html +=  '<label for="title" class="active" style="font-size:14px;">公司抬头:</label>';
                  _html += '</div>';
                  _html += '<div class="input-field">';
                  _html +=  '<input id="billing_code" type="number" class="validate" style="font-size:16px;" value="'+ pageData[0].tfn +'">';
                  _html +=  '<label for="billing_code" class="active" style="font-size:14px;">公司税号:</label>';
                  _html += '</div>';
                  _html += '</div>';
                  $('#row').append(_html);
              }
                title = $("#title").val();
                billing_code = $("#billing_code").val();
              // 填写发票信息显示和隐藏
              $('#row').on('click',"#test1",function(){
                $(".billing-wrap").show();
              }).on('click','#test2',function(){
                $(".billing-wrap").hide();
              });

              // 获取所有收货地址列表
              for(var i =0 ;i<pageData.length;i++){
                modal2_html += '<div class="bill-addr-wrap">';
                modal2_html += '<div class="bill-addr-title">';
                modal2_html += '<p>公司抬头:</p><p class="bill-addr-name">'+ pageData[i].company_title +'</p>';
                modal2_html += '</div>';
                modal2_html += '<div class="bill-addr-title">';
                modal2_html += '<p>公司税号:</p><p class="bill-addr-tfn">'+ pageData[i].tfn +'</p>';
                modal2_html += '</div>';
                modal2_html += '</div>';
              }
              $("#modal2").append(modal2_html);
              // 点击切换发票信息
              $("#modal2").on('click','.bill-addr-wrap',function(){
                var title = $('.bill-addr-name',$(this)).text();
                var billing_code = $('.bill-addr-tfn',$(this)).text();
                $("#title").val(title);
                $("#title").next().addClass('active');
                $("#billing_code").val(billing_code);
                $("#billing_code").next().addClass('active');
                $("#modal2").modal('close');
              });
          }
        })
      };

});
