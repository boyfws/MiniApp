
const GetHandleCardClick = (setterForScrollPosition, history) => (restaurant) => {
  setterForScrollPosition(window.scrollY);
  history.push(`/restaurant/${restaurant.id}`);
};


export default GetHandleCardClick;