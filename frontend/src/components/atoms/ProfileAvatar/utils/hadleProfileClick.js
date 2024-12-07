const GetHandleProfileClick = (setterForScrollPosition, history) => () => {
    setterForScrollPosition(window.scrollY);
    history.push(`/profile`);
  };


export default GetHandleProfileClick;