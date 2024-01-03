

function addToCart(id, name, price){
    fetch("/api/cart",{
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        return res.json();
    }).then(function(data){
        let carts = document.getElementsByClassName('cart-counter');
        for(let c of carts)
            c.innerText = data.total_quantity;
        let theADatHang = document.getElementById(`btn_a_${id}`)
        theADatHang.innerText = 'DONE✅';
        theADatHang.style.backgroundColor = 'green';
    })
}

function updateCart(id, obj){

//alert('xin chao')
//fetch(`/api/cart/${id}`,{
//        method: "put",
//        body: JSON.stringify({
//            "start": obj.value,
//            "end": obj.value
//
//        }),
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    }).then(function(res){
//        return res.json();
//    }).then(function(data){
//        let carts = document.getElementsByClassName('cart-counter');
//        for(let c of carts)
//            c.innerText = data.total_quantity;
//        let amounts = document.getElementsByClassName('cart-amount');
//        for(let c of amounts)
//            c.innerText = data.total_amount.toLocaleString("en");
//
//    })
}
function deleteCart(id){
    if(confirm("Bạn muốn xoá khỏi giỏ hàng?") === true){
    fetch(`/api/cart/${id}`,{
        method: "delete"
    }).then(function(res){
        return res.json();
    }).then(function(data){
        let carts = document.getElementsByClassName('cart-counter');
        for(let c of carts)
            c.innerText = data.total_quantity;
        let amounts = document.getElementsByClassName('cart-amount');
        for(let c of amounts)
            c.innerText = data.total_amount.toLocaleString("en");
    let t = document.getElementById(`room${id}`);
    t.style.display = "none";
    })
    }
}
