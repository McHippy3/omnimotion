export default function resizeDataURL(datas, wantedWidth, wantedHeight) {
  return new Promise(async function (resolve, reject) {

    // We create an image to receive the Data URI
    var img = document.createElement('img');

    // When the event "onload" is triggered we can resize the image.
    img.onload = function () {
      // We create a canvas and get its context.
      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');

      // We set the dimensions at the wanted size.
      canvas.width = wantedWidth;
      canvas.height = wantedHeight;

      // We resize the image with the canvas method drawImage();
      ctx.drawImage(this, 0, 0, wantedWidth, wantedHeight);

      var dataURI = canvas.toDataURL();

      // This is the return of the Promise
      resolve(dataURI);
    };

    // We put the Data URI in the image's src attribute
    img.src = datas;

  })
}