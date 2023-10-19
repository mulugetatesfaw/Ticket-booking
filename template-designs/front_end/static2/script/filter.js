const cardTemplate =
  '' +
  '<div' +
  '    class="col-12 col-md-6 col-lg-4"' +
  '        style="margin-top: 30px"' +
  '        data-aos="fade-up"' +
  '      >' +
  '        <div' +
  '          class="card card-hover shadow-lg p-3 mb-5 bg-white"' +
  '        >' +
  '          <img' +
  '            src="{{ image_url }}"' +
  '            class="card-img-top"' +
  '            alt="Image of {{ name }} hospital"' +
  '            style="height: 300px;' +
  '          />' +
  '          <div class="card-body">' +
  '            <h5 class="card-title">{{ name }} Hospital</h5>' +
  '            <p class="card-text">Card Price: ETB {{ card_price }}</p>' +
  '            <a' +
  '              href="/details?id={{ id }}&name={{ name }}"' +
  '              class="btn btn-success"' +
  '              style="border-radius: 20px"' +
  '              >See More</a' +
  '            >' +
  '          </div>' +
  '        </div>' +
  '      </div>';

const cardTemplateNew = $('template#hospital-template').html();

function addFilter(hospital) {
  return Mustache.render(cardTemplate, hospital);
}

$(function () {
  let cityId = [];
  let serviceId = [];

  $('a#all-cities-filter').click(function () {
    $('div.city-filter').empty();
    allHospital();
  });

  $('a#all-services-filter').click(function () {
    $('div.city-filter').empty();
    allHospital();
  });

  $('a#city_drop_downlink').click(function () {
    if ($(this).attr('data-type') === 'cities') {
      cityId[0] = $(this).attr('data-id');
      $('div.city-filter').empty();
      $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/hospital_search',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ cities: cityId }),
        success: function (data) {
          data.forEach((hospital) => {
            $('div.city-filter').append(addFilter(hospital));
          });
        },
      });
    }
  });

  $('a#service_drop_downlink').click(function () {
    if ($(this).attr('data-type') === 'services') {
      serviceId[0] = $(this).attr('data-id');
      $('div.city-filter').empty();
      $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/hospital_search',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ services: serviceId }),
        success: function (data) {
          data.forEach((hospital) => {
            $('div.city-filter').append(addFilter(hospital));
          });
        },
      });
    }
  });
  allHospital();
});

const allHospital = () => {
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/hospital_search',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({}),
    success: function (data) {
      data.forEach((hospital) => {
        $('div.city-filter').append(addFilter(hospital));
      });
    },
  });
};