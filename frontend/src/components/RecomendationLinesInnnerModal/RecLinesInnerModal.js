import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import React from 'react';


function sliceAndFill(array, size, filler) {
    const sliced = array.slice(0, size);
    
    while (sliced.length < size) {
      sliced.push(filler);
    }
  
    return sliced;
  }


const RECOM_LENGTH = 5 


const RecLinesInnerModal = ({ recomendations, onClick }) => {
    return (
      <div>
        {sliceAndFill(recomendations, RECOM_LENGTH, {"full_name": "Ggege"}).map((recom, index) => (
          <React.Fragment key={index}>
            <Cell onClick={() => onClick(recom)} className="recom-cell">
              <Text className="address-text">
              {recom.full_name}
              </Text>
            </Cell>
            {index < RECOM_LENGTH - 1 && <Divider />}
          </React.Fragment>
        ))}
      </div>
    );
  };
  
  export default RecLinesInnerModal;