// Пользовательский хук для доступа к объекту истории
const GetHandleCardClick = (history) => (restaurant) => {
  history.push(`/restaurant/${restaurant.id}`);
};


export default GetHandleCardClick;