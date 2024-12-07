// Css
import './SearchButton.css';

// Ext lib
import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// Handlers
import GetHandleSearchClick from './utils/handleSearchClick';

// Icon
import Icon24SearchOutline from '../../_icons/Icon24SearchOutline';


const SearchButton = ({ setSearchClicked }) => {
    const onSearchClick = GetHandleSearchClick(setSearchClicked)
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