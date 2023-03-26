import React from 'react'
import { Navigate, useParams } from 'react-router-dom'
import { Typography } from '@mui/material'
import { useTranslation } from 'react-i18next'

export default function ErrorPage() {

  const params = useParams()
  const [ t ] = useTranslation('translation',
      { keyPrefix: "errors.page_" + params.code})

  if (params.code === '401' || params.code === '403') {
    return <Navigate to='/login'/>
  }
  else {
    return (
      <div>
        <Typography variant='h2'>
          {t('title')}
        </Typography>
        <Typography variant="body1">
          {t('text')}
        </Typography>
      </div>
    )
  }
}
