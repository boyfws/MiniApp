const intersection_checker = (setA, setB) => {
    if (setA.size > setB.size) {
      [setA, setB] = [setB, setA];
    }

    for (let item of setA) {
      if (setB.has(item)) {
        return true; 
      }
    }
    return false; 
  };

  export default intersection_checker