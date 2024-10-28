import { Button, Input } from '@telegram-apps/telegram-ui';
import { Tappable } from '@telegram-apps/telegram-ui';
import { Icon24Close } from '@telegram-apps/telegram-ui/dist/icons/24/close';
import React, { useState } from 'react';
import './SearchForm.css';


const SearchForm = () => {

    const [query, setQuery] = useState('');

    const handleInputChange = (e) => {
        console.log(e.target.value);
        setQuery(e.target.value);
    };

    const handleClear = () => {
        setQuery('');
    };

    return (
        <div
        style={{backgroundColor: 'var(--tgui--bg_color)'}}>

        <Input 
        status="focused" 
        placeholder="Write and clean me" 
        value={query} 
        onChange={handleInputChange} 
        after={
            <Tappable 
            Component="div" 
            style={{display: 'flex'}}    
            onClick={handleClear}>
                <Icon24Close className='close-icon'/>
            </Tappable>
                } 
        className='input'
            />
        </div>

    )
}


export default SearchForm