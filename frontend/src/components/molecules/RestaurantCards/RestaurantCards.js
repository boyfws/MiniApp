// Css
import './RestaurantCards.css'

// Ext lib
import React, { useCallback, memo } from 'react';
import { useHistory } from "react-router-dom";

// State
import RestStore from "../../../state_management/stores/RestStore";

// Handlers
import GetHandleCardClick from './utils/handleRestCardClick';

// Component
import RestaurantCard from '../../atoms/RestaurantCard/RestaurantCard'


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