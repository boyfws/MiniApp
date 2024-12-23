// Css
import './LoaderComp.css'
import './Loading.css'


// Ext lib
import React, { useState, useEffect } from "react";
import {Steps} from "@telegram-apps/telegram-ui";


// Utils
import onFinishRestPage from './utils/onFinishRestPage'


// Ext lib


const SLOW_CHANGE_DURATION_MS = 1000; // Время для медленной фазы
const FAST_CHANGE_DURATION_MS = 500; // Время для быстрой фазы

const LoaderComp = ({ loading, onFinish, key }) => {
    const [progress, setProgress] = useState(0);
    const [startTime, setStartTime] = useState(null);
    const count = 10; // Количество шагов индикатора + 1


    useEffect(() => {
        let requestId = null;
        let duration = loading ? SLOW_CHANGE_DURATION_MS : FAST_CHANGE_DURATION_MS;

        const updateProgress = (timestamp) => {
            if (startTime === null) {
                setStartTime(timestamp);
            }
            const elapsed = timestamp - startTime;

            // Рассчитываем новый прогресс на основе прошедшего времени
            let newProgress = (elapsed / duration) * count;

            if (loading) {
                // Когда индикатор крутится бесконечно, сбрасываем прогресс после достижения максимума
                if (newProgress >= count) {
                    setStartTime(timestamp);
                    newProgress = 0; // Сбрасываем прогресс для бесконечного цикла
                }
                setProgress(newProgress);
                requestId = requestAnimationFrame(updateProgress); // Продолжаем бесконечную анимацию
            } else {
                // Когда загрузка завершена, плавно доводим до завершения
                setProgress(newProgress);
                if (newProgress < count) {
                    // Продолжаем анимацию, пока прогресс не достигнет максимума
                    requestId = requestAnimationFrame(updateProgress);
                } else {
                    // Завершаем анимацию, когда прогресс достиг максимума
                    setTimeout(onFinish, 0);
                }
            }
        };

        // Стартуем анимацию
        requestId = requestAnimationFrame(updateProgress);

        return () => {
            if (requestId) {
                cancelAnimationFrame(requestId); // Очищаем анимацию при размонтировании компонента
            }
        };
    }, [loading, onFinish, startTime]);

    // Округляем прогресс, чтобы он мог принимать значения от 0 до count, включая count
    const progressValue = Math.min(Math.round(progress), count);

    return (
        <Steps
            key={key}
            count={count}
            progress={progressValue}
            className="loading-indicator"
        />
    );
};




const Loader = ({onFinish, loading, key}) => {
    return (
        <div className="loading-wrapper">
            <LoaderComp loading={loading} onFinish={onFinish} key={key}/>
        </div>
    )
}





const LoaderWrapper = ({RestDataLoading, MenuLoading, setShowContent}) => {
    const onFinish = onFinishRestPage(setShowContent);
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        setLoading(RestDataLoading || MenuLoading);
    }, [RestDataLoading, MenuLoading]);


    return (
        <Loader loading={loading} onFinish={onFinish} key={2}/>
    )
}

export default LoaderWrapper;