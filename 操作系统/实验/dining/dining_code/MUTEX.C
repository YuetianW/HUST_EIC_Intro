/*
 * Mutex.c
 *
 * Sample code for "Multithreading Applications in Win32"
 * This sample is discussed in Chapter 4.
 *
 * Graphically demonstrates the problem of the
 * dining philosophers.
 *
 * This version uses mutexes with WaitForSingleObject(),
 * which can cause deadlock, and WaitForMultipleObjects(),
 * which always works properly.
 */

#define WIN32_LEAN_AND_MEAN
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <time.h>
#include "MtVerify.h"
#include "dining.h"


int PASCAL WinMain(HINSTANCE, HINSTANCE, LPSTR, int);
BOOL InitApplication(HINSTANCE);
BOOL InitInstance(HINSTANCE, int);

extern HWND   	hWndMain;			// Main Window Handle                             
extern BOOL bWaitMultiple;
extern BOOL bFastFood;

#define P_DELAY		bFastFood ? rand()/25 : ((rand()%5)+1)*1000 //控制进程时间

int gDinerState[PHILOSOPHERS];
int gChopstickState[PHILOSOPHERS];

HANDLE gchopStick[PHILOSOPHERS];	// 1 chopstick between each philopher and his neighbor

#undef PostMessage
#define PostMessage SendMessage

DWORD WINAPI PhilosopherThread(LPVOID pVoid)
{
	HANDLE myChopsticks[2];
	int iPhilosopher = (int) pVoid;
	int iLeftChopstick = iPhilosopher;
	int iRightChopstick = iLeftChopstick + 1;
	DWORD result;

	if (iRightChopstick > PHILOSOPHERS-1)  //筷子编号过了5就使它为0
		iRightChopstick = 0;

    //Randomize the random number generator
	srand( (unsigned)time( NULL ) * (iPhilosopher + 1) );

	// remember handles for my chopsticks
	myChopsticks[0] = gchopStick[iLeftChopstick];      //定义哲学家的左右筷子
	myChopsticks[1] = gchopStick[iRightChopstick];

	gDinerState[iPhilosopher] = RESTING;	//wants chopsticks

    Sleep(P_DELAY);

	for(;;)
	{
		if (bWaitMultiple == FALSE)
		{
			// Wait until both of my chopsticks are available
			gDinerState[iPhilosopher] = WAITING;	//wants chopsticks
            PostMessage(hWndMain, WM_FORCE_REPAINT,0 ,0); 
			result = WaitForSingleObject(gchopStick[iLeftChopstick], INFINITE);
			MTVERIFY(result == WAIT_OBJECT_0);
			gChopstickState[iLeftChopstick] = iPhilosopher;
			Sleep(P_DELAY/4);

			gDinerState[iPhilosopher] = WAITING;	//wants chopsticks
            PostMessage(hWndMain, WM_FORCE_REPAINT,0 ,0);
			result = WaitForSingleObject(gchopStick[iRightChopstick], INFINITE);
			MTVERIFY(result == WAIT_OBJECT_0);
			gChopstickState[iRightChopstick] = iPhilosopher;
		}
		else
		{
			// Wait until both of my chopsticks are available
			gDinerState[iPhilosopher] = WAITING;	//wants chopsticks
			PostMessage(hWndMain, WM_FORCE_REPAINT,0 ,0);
			result = WaitForMultipleObjects(2, myChopsticks, TRUE, INFINITE);
			MTVERIFY(result >= WAIT_OBJECT_0 && result < WAIT_OBJECT_0 + 2);
			gChopstickState[iLeftChopstick] = iPhilosopher;
			gChopstickState[iRightChopstick] = iPhilosopher;
		}

		// Philosopher can now eat a grain of rice
		gDinerState[iPhilosopher] = EATING;	//philosopher is eating
		PostMessage(hWndMain, WM_FORCE_REPAINT,0 ,0);
        Sleep(P_DELAY);

		// Put down chopsticks
		gDinerState[iPhilosopher] = RESTING;	//philosopher is resting
		gChopstickState[iRightChopstick] = UNUSED;
		gChopstickState[iLeftChopstick] = UNUSED;
		PostMessage(hWndMain, WM_FORCE_REPAINT,0 ,0);
		MTVERIFY( ReleaseMutex(gchopStick[iLeftChopstick]) ); //释放筷子资源
		MTVERIFY( ReleaseMutex(gchopStick[iRightChopstick]) );

		// Philosopher can now meditate
        Sleep(P_DELAY);

	} // end for

	return 0;
}

int Diner(void)
{
	HANDLE hThread[PHILOSOPHERS];
	DWORD dwThreadId;
	int i;

	for (i=0; i < PHILOSOPHERS; i++)
	{
		//Initialize the chopsitcks to unused
		gChopstickState[i] = UNUSED;
		// initialize the diner state table
		gDinerState[i] = 0;
		// The Philosophers prepare to eat
		gchopStick[i] = CreateMutex(NULL, FALSE, NULL); //建立互斥量
		MTVERIFY(gchopStick[i] != NULL);
	}

	for (i = 0; i < PHILOSOPHERS; i++)
		MTVERIFY( hThread[i] = CreateThread(NULL, 0, PhilosopherThread, (LPVOID) i, 0, &dwThreadId ));//启动进程

	return 0;
}
