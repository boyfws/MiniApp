// Css
import './RestaurantCard.css'

// Ext lib
import React, {memo} from "react";
import {Card} from "@telegram-apps/telegram-ui";


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


export default RestaurantCard;
