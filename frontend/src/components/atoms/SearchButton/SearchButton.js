import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './SearchButton.css';
import Icon24SearchOutline from '../../../icons/Icon24SearchOutline';
import GetHandleSearchClick from '../../../handlers/handleSearchClick';


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