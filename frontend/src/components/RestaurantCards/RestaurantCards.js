import React from 'react';
import { Card } from '@telegram-apps/telegram-ui';
import './RestaurantCards.css';


const RestaurantCards = ({ restaurants, onCardClick }) => {
  return (
    <div className="restaurant-cards">
      {restaurants.map((restaurant) => (
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
      ))}
    </div>
  );
};

export default RestaurantCards;