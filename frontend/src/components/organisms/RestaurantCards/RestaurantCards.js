import React, { useCallback, memo } from 'react';
import { Card } from '@telegram-apps/telegram-ui';
import './RestaurantCards.css';
import GetHandleCardClick from '../../../handlers/handleRestCardClick';
import RestStore from "../../../stores/RestStore";
import {useHistory} from "react-router-dom";


const RestaurantCard = memo(({ restaurant, onCardClick }) => (
  <Card key={restaurant.id} onClick={() => onCardClick(restaurant)} className="restaurant-card">
    <React.Fragment key={restaurant.id}>
      {restaurant.tag && (
        <Card.Chip className="card-chip" readOnly>
          {restaurant.tag}
        </Card.Chip>
      )}
      <div className="image-container">
        <img
          alt={restaurant.name}
          src={restaurant.image}
          className="restaurant-image"
        />
      </div>
      <Card.Cell readOnly subtitle={`${restaurant.distance} km`} className="card-cell">
        {restaurant.name}
      </Card.Cell>
    </React.Fragment>
  </Card>
));

const RestaurantCards = ({ setScrollPositionY}) => {
  const { filteredRestaurants } = RestStore()
  const history = useHistory();
  const onCardClick = GetHandleCardClick(setScrollPositionY, history)

  const handleCardClick = useCallback((restaurant) => {
    onCardClick(restaurant);
  }, [onCardClick]);

  return (
    <div className="restaurant-cards">
      {filteredRestaurants.map((restaurant) => (
        <RestaurantCard
          key={restaurant.id}
          restaurant={restaurant}
          onCardClick={handleCardClick}
        />
      ))}
    </div>
  );
};

export default RestaurantCards;