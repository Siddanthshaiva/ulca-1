const GlobalStyles = (theme) => ({
  container: {
    
    maxWidth: "1272px",
    width : "100%",
    margin :"0 auto",
    // background: theme.palette.background.default,
    fontFamily: theme.typography.fontFamily
  },

  headerContainer :{
    border :"1 solid green",
    height:"54px"
  }
  // root: {



  // },
  // appBar: {
  //   backgroundColor: theme.palette.primary.dark,
  //   zIndex: theme.zIndex.drawer + 1,
  //   transition: theme.transitions.create(["width", "margin"], {
  //     easing: theme.transitions.easing.sharp,
  //     duration: theme.transitions.duration.leavingScreen,
  //   }),
  // },
  // content: {
  //   background: theme.palette.background.default,
  //   flexGrow: 1,
  //   backgroundColor: theme.palette.background.default,
  //   padding: theme.spacing(3),
  //   marginTop: "3%",
  // },
  // loaderStyle: {
  //   position: 'fixed',
  //   backgroundColor: 'rgba(0, 0, 0, 0.5)',
  //   zIndex: 1000,
  //   width: '100%',
  //   height: '100%',
  //   top: 0,
  //   left: 0,

  // },
  // progress: {
  //   position: 'relative',
  //   top: '40%',
  //   left: '46%'

  // },
  // snackbar: {
  //   width: '100%',
  //   marginTop:"50px",
  //   '& > * + *': {
  //     marginTop: "50px",
  //   },
  // },
  // snackbarFont: {
  //   fontSize: '1rem'
  // }
});

export default GlobalStyles;
