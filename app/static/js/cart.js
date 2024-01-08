const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const todayString = `${year}-${month}-${day}`;
const regularDay = '28';
function constraintRegularDay(stringA, stringB, regularDay)
{
    var a = new Date(stringA)
    var b = new Date(stringB)

    var times = b.getTime() - a.getTime();
    var days = Math.ceil(times / (1000 * 3600 * 24) );
    if (days > parseInt(regularDay))
        return false;
    if (days <= parseInt(regularDay))
        return true;

}
function compareDateString(stringA, stringB)
{
    var a = new Date(stringA)
    var b = new Date(stringB)


    var dateA = a.toISOString().split('T')[0];
    var dateB = b.toISOString().split('T')[0];
    if (dateA>dateB)
        return 1;
    if (dateA<dateB)
        return -1;
    if (dateA === dateB)
        return 0;

}
function compareStringWithToday(dateString)
{
    var cd = new Date();
    var currentDate = cd.toISOString().split('T')[0];
    var id = new Date(dateString);
    var inputDate = id.toISOString().split('T')[0];
    if (inputDate < currentDate)
        return false;
    else
        return true;
}

function addToCart(id, name, price){
    fetch("/api/cart",{
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price,
            "start": '',
            "end": ''

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
        theADatHang.innerText = 'DONE!';
        theADatHang.style.backgroundColor = 'green';
    })
}



function updateCartEnd(id, obj){
    var input = document.getElementById(`ipe${id}`).value;
    var output = document.getElementById(`ips${id}`).value;
    var regex = /^\d{4}-\d{2}-\d{2}$/;
    let tmp = true;
    var inputErr = document.getElementById(`ipe${id}`);



    if(!regex.test(input))
    {
         inputErr.classList.add("err");
         inputErr.value = 'YYYY-MM-DD';
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
     }

    if(compareStringWithToday(input) === false)
    {
        inputErr.value = 'Date is too early';
        inputErr.classList.add("err")
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
    }
    if(compareDateString(input,output) === -1)
    {
        inputErr.value = 'End is earlier than Start';
        inputErr.classList.add("err")
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
    }
        if (regex.test(input) && compareStringWithToday(input) && (compareDateString(input,output) === 0||compareDateString(input,output) === 1))
        {
        let inputErr = document.getElementById(`ipe${id}`);
        inputErr.classList.remove("err");
        }

        let a = document.getElementsByClassName("ipDate");
        let t = parseInt('0');
        for(let i = 0; i < a.length; i++)
        {
             if (!regex.test(a[i].value))
             {
             t++;
             }
        }
        if (t===0)
            {
            let btnP = document.getElementById("btn-purchase");
            btnP.disabled = false;
            }


    fetch(`/api/cart/${id}`, {
        method: "put",
        body: JSON.stringify({
            "end": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName('cart-amount');
        for (let c of amounts)
            c.innerText = data.total_amount.toLocaleString("en");
    });
}
function updateCartStart(id, obj) {

    var input = document.getElementById(`ips${id}`).value;
    var output = document.getElementById(`ipe${id}`).value;
    var regex = /^\d{4}-\d{2}-\d{2}$/;
    let tmp = true;
    var inputErr = document.getElementById(`ips${id}`);
    let cd = new Date();
    let currentDate = cd.toISOString().split('T')[0];


    if(!regex.test(input) || !constraintRegularDay(currentDate,input,regularDay))
    {
         inputErr.classList.add("err");
         inputErr.value = 'YYYY-MM-DD';
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
     }

    if(compareStringWithToday(input) === false)
    {
        inputErr.value = 'Date is too early';
        inputErr.classList.add("err")
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
    }
    if(compareDateString(input,output) === 1)
    {
        inputErr.value = 'Start is later than End';
        inputErr.classList.add("err")
         let btnP = document.getElementById("btn-purchase");
         btnP.disabled = true;
    }

    if (regex.test(input) && compareStringWithToday(input) && (compareDateString(input,output) === 0||compareDateString(input,output) === -1) && constraintRegularDay(currentDate,input,regularDay) )
     {
     let inputErr = document.getElementById(`ips${id}`);
     inputErr.classList.remove("err");
     }

        let a = document.getElementsByClassName("ipDate");
        let t = parseInt('0');
        for(let i = 0; i < a.length; i++)
        {
             if (!regex.test(a[i].value))
             {
             t++;
             }
        }
        if (t===0)
            {
            let btnP = document.getElementById("btn-purchase");
            btnP.disabled = false;
            }

    fetch(`/api/cart/start/${id}`, {
        method: "put",
        body: JSON.stringify({
            "start": obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {

        let carts = document.getElementsByClassName('cart-counter');
        for (let c of carts)
            c.innerText = data.total_quantity;

        let amounts = document.getElementsByClassName('cart-amount');
        for (let c of amounts)
            c.innerText = data.total_amount.toLocaleString("en");
    });
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
function pay() {
    if (confirm("Bạn muốn đặt phòng như trên?") === true) {
        fetch("/api/pay", {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                {
                    alert('Đặt phòng thành công')
                    location.reload();
                }

            else
                alert('Lỗi')
        })
    }
}


