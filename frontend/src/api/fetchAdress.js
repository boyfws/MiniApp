import fetchWithRetry from "../queries/GET_query";

/**
 * Функция предназначена для получения данных в формате GeoJSON, содержащих информацию об одном адресе.
 * 
 * @returns {Object} Объект с двумя ключами:
 *   - 'error': {boolean} Флаг, указывающий на наличие ошибки. Если true, значит произошла ошибка, и данные недоступны.
 *   - 'data': {Object} Объект с данными в формате GeoJSON. Если ошибка произошла, этот ключ будет содержать пустой объект или null.
 * 
 * Формат данных:
 *   - 'type': {string} Тип геометрии (например, 'Feature').
 *   - 'geometry': {Object} Геометрические данные, содержащие координаты адреса.
 *     - 'type': {string} Тип геометрии (например, 'Point').
 *     - 'coordinates': {Array} Массив с координатами [longitude, latitude].
 *   - 'properties': {Object} Свойства адреса, содержащие следующие поля:
 *     - 'street': {string} Название улицы.
 *     - 'house': {string} Номер дома.
 *     - 'district': {string} Район.
 *     - 'city': {string} Город.
 * 
 * Пример возвращаемых данных:
 * {
 *   error: false,
 *   data: [{...}, {...}, {...}]
 * }
 * Пример GEOJSON-данных:
 * {
 *    type: 'Feature',
 *    geometry: {
        type: 'Point',
        coordinates: [37.587914, 55.783954]
      },
      properties: {
        street: 'Поликарпова',
        house: '1',
        district: 'Хорошёвский',
        city: 'Москва'
      }
 */
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));


const fetchAdress = async (id) => {
    const def_adress = {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [37.587914, 55.783954]
      },
      properties: {
        street: 'Поликарпова',
        house: '1',
        district: 'Хорошёвский',
        city: 'Москва'
      }
    }
    await sleep(1000)
    return {
           error: false,
           data: [def_adress, def_adress, def_adress]
          }
         }


export default fetchAdress



