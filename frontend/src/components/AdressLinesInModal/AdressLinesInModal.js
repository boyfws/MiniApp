import React from 'react';
import { Cell, Divider } from '@telegram-apps/telegram-ui';

const AdressLinesInModal = ({ adresses, onClick }) => {
  return (
    <div>
      {adresses.map((address, index) => (
        <React.Fragment key={index}>
          <Cell onClick={() => onClick(address)}>
            {address?.city ?? ''} {adress?.district ?? ''} {address?.street ?? ''} {address?.house ?? ''}
          </Cell>
          {index < adresses.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </div>
  );
};

export default AdressLinesInModal;