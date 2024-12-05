import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './SearchButton.css';
import Icon24SearchOutline from '../../icons/Icon24SearchOutline';


const SearchButton = ({ onSearchClick }) => {
    return (
        <Button 
            size="s" 
            mode="bezeled" 
            onClick={onSearchClick}
            className='search-button' >
            <Icon24SearchOutline  className='icon'/>
        </Button>
    );
}

export default SearchButton;