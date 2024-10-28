// Пользовательский хук для доступа к объекту истории
const GetHandleCardClick = (history, setterForScrollPosition) => (restaurant) => {
  setterForScrollPosition(window.scrollY);
  history.push(`/restaurant/${restaurant.id}`);
};


export default GetHandleCardClick;