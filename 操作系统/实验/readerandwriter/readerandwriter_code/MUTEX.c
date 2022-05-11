/*
 * Mutex.c
 *
 * Sample code for "Multithreading Applications in Win32"
 * This sample is discussed in Chapter 4.
 *
 * Graphically demonstrates the problem of the
 * ReaderAndWriter.
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
#include "ReaderAndWriter.h"


int PASCAL WinMain(HINSTANCE, HINSTANCE, LPSTR, int);
BOOL InitApplication(HINSTANCE);
BOOL InitInstance(HINSTANCE, int);

extern HWND   	hWndMain;			// Main Window Handle                             


#define P_DELAY	 rand()/25*10


int Readercount;                       //the number of reader
int readerstate[CCounter];             //the state of reader
int writerstate[CCounter];             //the state of writer
int resourcestate[CCounter];           //the state of resource
CRITICAL_SECTION  RP_Write;            //the variable used to identify the Critical Section
HANDLE count;                          //the resouce used to define the readcount 
#undef PostMessage
#define PostMessage SendMessage

DWORD WINAPI ReaderThread(LPVOID pVoid)
{
	int ReaderNum = (int)pVoid;  // get the number of thread(reader)          
	DWORD result;
	//Randomize the random number generator
	srand((unsigned)time(NULL) * (ReaderNum + 1));
	readerstate[ReaderNum] = resting;        //reader is resting
	Sleep(P_DELAY);
	for (;;)
	{// Wait until resources are available
		readerstate[ReaderNum] = waiting;    //reader is waiting
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		result = WaitForSingleObject(count, INFINITE);  //get the resource of count
		if (result == WAIT_OBJECT_0)
			Readercount += 1;
		if (Readercount == 1)
			EnterCriticalSection(&RP_Write);  //get the critical section
		MTVERIFY(ReleaseMutex(count));        // release the resource of count
		resourcestate[ReaderNum] = read;
		readerstate[ReaderNum] = reading;     //the reader is reading
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		Sleep(P_DELAY / 4);

		result = WaitForSingleObject(count, INFINITE); //get the resource of count
		if (result == WAIT_OBJECT_0)
			Readercount -= 1;
		if (Readercount == 0)
			LeaveCriticalSection(&RP_Write);     //leave the cristical section
		MTVERIFY(ReleaseMutex(count));           //release the resource of count
		readerstate[ReaderNum] = resting;        //the reader is reading 
		resourcestate[ReaderNum] = UNUSED;
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		Sleep(P_DELAY);
	}
	return 0;
}
DWORD WINAPI WriterThread(LPVOID pVoid)
{
	int writerNum = (int)pVoid;   // get the nunber of thread(writer)
   //Randomize the random number generator
	srand((unsigned)time(NULL) * (writerNum + 1));
	writerstate[writerNum] = resting;  //the writer id resting
	Sleep(P_DELAY);
	for (;;)
	{ // Wait until resources are available
		writerstate[writerNum] = waiting;   //the writer is waiting
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		EnterCriticalSection(&RP_Write);   // enter the critical section
		writerstate[writerNum] = writing;  // the writer is writing
		resourcestate[writerNum] = write;
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		Sleep(P_DELAY / 4);
		LeaveCriticalSection(&RP_Write);   //leave the critical section
		writerstate[writerNum] = resting;  // the writer is resting
		resourcestate[writerNum] = UNUSED;
		PostMessage(hWndMain, WM_FORCE_REPAINT, 0, 0);
		Sleep(P_DELAY);
	}
	return 0;
}

int ReaderAndWriter(void)
{
	HANDLE hThread[CCounter];
	HANDLE hThread1[CCounter];
	DWORD dwThreadId;
	int i;
	Readercount = 0;
	resourcestate[CCounter] = UNUSED;
	count = CreateMutex(NULL, FALSE, NULL);
	MTVERIFY(count != NULL);
	InitializeCriticalSection(&RP_Write);  //initialize the critical section
	for (i = 0; i < CCounter; i++)
	{//inlitialize the reader and writer state
		readerstate[i] = resting;
		writerstate[i] = resting;
	}

	for (i = 0; i < CCounter; i++)
	{   //creat the reader and writer thread
		MTVERIFY(hThread[i] = CreateThread(NULL, 0, ReaderThread, (LPVOID)i, 0, &dwThreadId));
		MTVERIFY(hThread1[i] = CreateThread(NULL, 0, WriterThread, (LPVOID)i, 0, &dwThreadId));
	}
	return 0;
}