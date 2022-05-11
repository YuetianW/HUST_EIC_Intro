/********************************************************/
/* Dining.h - Application Prototypes & Definitions       */
/********************************************************/

// Dining Philosophers Globals
#define UNUSED			-1
#define RESTING         0
#define WAITING         1
#define EATING          2

#define PHILOSOPHERS    5       // Number of philosophers

#define WM_FORCE_REPAINT WM_APP+10
#define CM_EXIT         1000
		
int Diner(void);


