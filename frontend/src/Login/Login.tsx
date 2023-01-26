import { useTranslation } from 'react-i18next';


function Login() {
  const {t, i18n} = useTranslation();
  return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    }}>
        <p>{t('title')}</p>
        <form onSubmit={(e) => {i18n.changeLanguage(i18n.language === 'en' ? 'ru' : 'en'); e.preventDefault()}}>
          <input type="submit" value="Submit"/>
        </form>
      </div>
    )
}

export default Login;