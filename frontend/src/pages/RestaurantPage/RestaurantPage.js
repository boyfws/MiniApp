// Css
import './RestaurantPage.css'

// Ext lib
import React, {useEffect, useState} from 'react';
import { useHistory, useParams } from 'react-router-dom';

// Comp
import LoaderWrapperRestPage from "../../components/templates/LoaderWrapperRestPage/LoaderWrapperRestPage";
import RestPageTemp from "../../components/templates/RestPageTemp/RestPageTemp";

// Utils
import GetLoadRestData from "./utils/LoadRestData";
import GetHandleGoBack from "./utils/handleGoBack";
import GetLoadMenu from "./utils/LoadMenu";
import {Cell, Rating, Subheadline, Title, Text, Divider} from "@telegram-apps/telegram-ui";
import PreapareGeoJsonForDisplay from "../../components/atoms/RestAddressTitle/utils/PrepareGeoJsonForDisplay";


const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const [RestData, SetRestData] = useState({});
  const [Menu, setMenu] = useState({});

  const [RestDataLoading, setRestDataLoading] = useState(true);
  const [MenuLoading, setMenuLoading] = useState(true);


  const [showContent, setShowContent] = useState(false);

  
  const LoadRestData = GetLoadRestData(
      setRestDataLoading,
      id,
      SetRestData
  );

  const LoadMenu = GetLoadMenu(
      setMenuLoading,
      id,
      setMenu);

  const handleGoBack = GetHandleGoBack(history);



  useEffect(() => {
      window.Telegram.WebApp.BackButton.onClick(handleGoBack);
      window.Telegram.WebApp.BackButton.show()
  }, [])


  useEffect(LoadRestData, [])

  useEffect(LoadMenu, [])


  if (!showContent) {
    return (
        <LoaderWrapperRestPage
            RestDataLoading={RestDataLoading}
            MenuLoading={MenuLoading}
            setShowContent={setShowContent}
        />
    )
  }

  return (
    <div className="RestaurantPage">
      <div className={"header"}>

        <Title level="2" weight="1" plain={false} style={{padding: 0}}>
          {RestData.name}
        </Title>

        <Subheadline className="subheadline">
          {PreapareGeoJsonForDisplay(RestData.address)}
        </Subheadline>

        <Divider/>

      </div>

      <div className="photos">
        Тут типа будут фотки (сори решили сделать хоть как то, так как красиво не успели)
      </div>

      <Divider/>

      <div className="raiting-wrapper">
        <Cell className="raiting-cell"
              onClick={() => (window.Telegram.WebApp.openLink(RestData.ext_serv_link_1))}>
          <Text
              className="raiting-cell-text"
          >
            Яндекс карты

          </Text>

          <Rating
              max={5}
              precision={0.1}
              value={RestData.ext_serv_rank_1}
              onChange={() => {}}
              className="raiting"
              disabled={true}
          />

        </Cell>
      </div>

      <Divider/>



    </div>
  );
};

export default RestaurantPage;