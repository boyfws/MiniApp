import { Icon28Close } from "@telegram-apps/telegram-ui/dist/icons/28/close";
import { IconContainer} from "@telegram-apps/telegram-ui";

const BackButton = ({ onBackspace }) => {
    return (
        <IconContainer>
            <Icon28Close onClick={onBackspace}/>
        </IconContainer>
    )
}

export default BackButton