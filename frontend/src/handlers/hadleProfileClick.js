const GetHandleProfileClick = (history, setterForScrollPosition) => () => {
    setterForScrollPosition(window.scrollY);
    history.push(`/profile`);
  };
  
  
  export default GetHandleProfileClick;