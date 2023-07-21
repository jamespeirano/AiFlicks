const button = document.getElementById('buy_button');

button.addEventListener('click', (e) => {
  e.preventDefault();

  // Get the image source
  const base64_image = document.getElementsByClassName('generated-image')[0].children[0].src; 
  // const apiKey = 'P3sbXrqgozFxB1SwZaFbCYwiKIL7Jy6g8rDcHRUj';
  const apiKey = 'UsvITXFcmE85ijtvob38Ld9Z0Ihym4dcWjYicRvZ'           // store api key
  
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      image_url: base64_image,
      item_code: "RNA4",
      name: "Your AI Design",
      colours: "Black,White,Red,Blue,Green,Yellow,Pink,Purple,Orange,Brown,Gray",
      description: "Check out your AI generated design on a t-shirt! Scroll down to see more products and variations.",
      currency: "USD"
    }),
  };
  
  var newTab = window.open('about:blank', '_blank');
  newTab.document.write(
    "<body style='background-color:#faf9f9;width:100%;height:100%;margin:0;position:relative;'><img src='https://storage.googleapis.com/teemill-dev-image-bucket/doodle2tee_loader.gif' style='position:absolute;top:calc(50% - 100px);left:calc(50% - 100px);'/></body>"
  );


  fetch('https://aiflix.teemill.com/omnis/v3/product/create', options)
    .then(response => response.json())
    .then(response => newTab.location.href = response.url)
    .catch(err => console.error(err));
});