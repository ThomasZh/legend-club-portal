// @2017/07/05
$(function(){

      var api_domain = $("#api_domain").val();
      var access_token = $("#access_token").val();
      var club_id = $("#club_id").val();
      function getCartPro(pageNum) {
          var limit = 20;//初始化值
          $.ajax({
            type: "GET",
            url: api_domain+"/api/clubs/"+ club_id +"/cart/items?page="+pageNum+"&limit="+limit,
            headers: {"Authorization": "Bearer "+ access_token +""},
            contentType: 'application/json',
            success: function(data, status, xhr) {

                  data_obj = JSON.parse(data);
                  data = data_obj.rs;
              var pageData = data.data;
              var inner_html = "";
              // console.log(pageData);
              for (var i in pageData) {
                  inner_html += '<li class="collection-item avatar list-item-info">';
                  inner_html += '<img src="'+ pageData[i].img +'" alt="" class="circle">';
                  inner_html += '<span class="title" data_pro_id="'+pageData[i].item_id+'">'+pageData[i].title+'</span>';
                  inner_html += '<p>规格: '+pageData[i].spec_title+'</p>';
                  inner_html += '<div class="hilight flex-separate">';
                  inner_html += '<input type="hidden" value="'+ pageData[i].spec_id +'" class="spec_template">';
                  inner_html += '<span class="one-price">'+pageData[i].amount/100+'元/桶</span>';
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
                function getTotal(){
                  var num = $(".list-item-info").length;
                  var total_price=0;
                  for(var i=0;i<num;i++){
                    var one_price = $(".list-item-info").eq(i).find(".one-price").text();
                    // console.log(one_price);
                    var quantity = $(".list-item-info").eq(i).find(".one-quantity").text();
                    // console.log(quantity);
                    var one_total = parseFloat(one_price)*quantity;
                        total_price += parseFloat(one_total);
                  }
                    // $(".footer-total-price").children().html(total_price.toFixed(2));
                    $("#footer-bar span").text(total_price.toFixed(2));
                    $("#total_amount").val(total_price.toFixed(2));
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
                 $("#item_input").val(JSON.stringify(items));

                // 收货地址
               var address = {};
                 // 保存地址到localstorage

               if(!window.localStorage){
                     alert("浏览器不支持localstorage");
                     return false;
                 }else{
                   function getLoaclData(){
                     var storage=window.localStorage;
                     var name = storage.getItem("name");
                     var phone = storage.getItem("phone");
                     var l_addr = storage.getItem("addr");
                     $("#t_name").html(name);
                     $("#t_phone").html(phone);
                     $("#t_address").html(l_addr);

                    //  var name = $("#t_name").html();
                    //  var phone = $("#t_phone").html();
                    //  var addr = $("#t_address").html();
                     address = {"name":name,"phone":phone,"addr":l_addr};
                     $("#addr_input").val(JSON.stringify(address));

                   };
                   getLoaclData();
                   $("#add-btn").on('click',function(){
                     var storage=window.localStorage;
                     var name = $("#name").val()?$("#name").val():storage.getItem("name");
                     var phone = $("#phone").val()?$("#phone").val():storage.getItem("phone");
                     var addr = $("#addr").val()?$("#addr").val():storage.getItem("addr");
                         name = (name == null)?'':name;
                         phone = (phone == null)?'':phone;
                         addr = (addr == null)?'':addr;
                         storage["name"]=name;
                         storage["phone"]=phone;
                         storage["addr"]=addr;
                         $(".z-depth-1").css('display',"none");
                         getLoaclData();
                   });
                 };

                // 下单操作
                $("#sub-order").on('click',function(event){
                  console.log(address);
                  if(items.length == 0){
                    $.alert('您还没有选择任何商品!')
                     event.preventDefault();
                  }else if(address.name == null || address.name == '' || address.phone == '' || address.addr == ''){
                    $.alert("请填写收货地址!");
                    event.preventDefault();
                  }
                  else{
                    $(".order-form").submit();
                  }

                });

              }
            })
      };
      getCartPro('1');

});
