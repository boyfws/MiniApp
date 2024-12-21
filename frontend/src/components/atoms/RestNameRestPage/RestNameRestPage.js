import { Title } from "@telegram-apps/telegram-ui";

const RestNameRestPage = ({name}) => {
    return (
        <Title level="2" weight="1" plain={false} style={{padding: 0}}>
            {name}
        </Title>
    )

}

export default RestNameRestPage;