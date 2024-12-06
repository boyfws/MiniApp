import './UpperLevelMainPage.css'

import SearchForm from '../../components/SearchForm/SearchForm';
import AddressButton from '../AddressButton/AdressButton';
import SearchButton from '../../components/SearchButton/SearchButton';
import ProfileAvatar from '../../components/ProfileAvatar/ProfileAvatar';

import GetLoadRestFromSearch from '../../webhooks/GetNewRestFromSearch';

import { Context } from "../../Context";

import React, { useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";


const UpperLevelMainPage = ({setRestaurants, setScrollPositionY, defaultRestaurants, setModalState}) => {
    const [searchClicked, setSearchClicked] = useState(false);
    const [InputValue, setInputValue] = useState('');

    const history = useHistory();

    const { DefAddress } = useContext(Context);


    const LoadRestFromSearch = GetLoadRestFromSearch(
        DefAddress,
        InputValue, 
        setRestaurants
      );

    useEffect(LoadRestFromSearch, [InputValue]);




    return (
        <div className="upper-level-wrapper">
            <div className={`upper-level${searchClicked ? '-hidden' : ''}`}>
                <ProfileAvatar
                    setScrollPositionY={setScrollPositionY}
                    history={history}
                    className='profile-avatar'
                />

                <AddressButton
                    defaultAdress={DefAddress}
                    className='adress-button'
                    onClick={() => {setModalState(true)}}
                />


                <SearchButton 
                    setSearchClicked={setSearchClicked} 
                    className='search-button' 
                />

            </div>

            <div className={`search${searchClicked ? '' : '-hidden'}`}>
                <SearchForm 
                    setRestaurants={setRestaurants} 
                    setSearchClicked={setSearchClicked}
                    defaultRestaurants={defaultRestaurants}
                    ChangeValueInMainPage={setInputValue}/>
            </div>

      </div>
    )
}


export default UpperLevelMainPage