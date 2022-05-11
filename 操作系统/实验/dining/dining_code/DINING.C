/*
 * Dining.c
 *
 * Sample code for "Multithreading Applications in Win32"
 * This sample is discussed in Chapter 4.
 *
 * Graphically demonstrates the problem of the
 * dining philosophers.
 */

#define WIN32_LEAN_AND_MEAN
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <windowsx.h>
#include <string.h>
#include <math.h>
#include "dining.h"

HINSTANCE 	hInst;			// Application Instance Handle
HWND   	hWndMain;       	// Main Window Handle                             
HBITMAP	hbmpOffscreen;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void RenderOffscreen(HDC hDestDC);

BOOL bWaitMultiple;
BOOL bFastFood;

extern int gDinerState[];
extern int gChopstickState[];
extern HANDLE gchopStick[PHILOSOPHERS];	// 1 chopstick between each philosopher and his neighbor
 
/********************************************************************/
/*	ROUTINE:	WndProc												*/
/*																	*/
/*	PURPOSE:	Processes messages									*/
/********************************************************************/

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, 
	WPARAM wParam, LPARAM lParam)
{
	PAINTSTRUCT ps;
	HDC hdc;

	switch (message) 
	{
		case WM_COMMAND:
			switch (wParam) 
			{
			case CM_EXIT:
				PostMessage(hWndMain, WM_CLOSE, 0, 0L);
				break;  
			} 
			break;

		case WM_FORCE_REPAINT:
			{
				MSG msg;

				InvalidateRect(hWndMain, NULL, TRUE);
				while (PeekMessage(&msg, hWndMain, WM_FORCE_REPAINT,WM_FORCE_REPAINT,TRUE))
					;
			}
			break;

		case WM_PAINT:
			
			hdc = BeginPaint(hWndMain, &ps);

			RenderOffscreen(hdc);
			
			EndPaint(hWndMain, &ps);
			break;

		case WM_CLOSE:
			return DefWindowProc(hWndMain, message, wParam, lParam);

		case WM_DESTROY:
			PostQuitMessage(0);
			break;

		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
}
	return (0);
}

BOOL CreateOffscreen()
{
	HWND hwndScreen = GetDesktopWindow();
	HDC hdc	= GetDC(hwndScreen);

	int	nWidth	= GetSystemMetrics( SM_CXSCREEN );
	int	nHeight	= GetSystemMetrics( SM_CYSCREEN );

	hbmpOffscreen = CreateCompatibleBitmap( hdc, nWidth, nHeight );

	ReleaseDC(hwndScreen, hdc);

	if ( !hbmpOffscreen )
		return FALSE;
	else
		return TRUE;
}

void RenderOffscreen(HDC hDestDC)
{
	HDC hdc				= hDestDC; // CreateCompatibleDC(hWndMain);
	int err=GetLastError();
	HBITMAP hOldBitmap	= SelectObject(hdc, hbmpOffscreen);
	RECT rect;
	HPEN hPen;
	double dx, dy, px, py,  AngRad, dDeltaAng;
	int pos, p1;
	long CenterX, CenterY;

	hPen = SelectObject(hdc, CreatePen(PS_SOLID, 3, 0L));

	GetClientRect(hWndMain, &rect);

	/* Draw the table */
	CenterX = (rect.right - rect.left)/2;
	CenterY = (rect.bottom - rect.top)/2;
	Ellipse(hdc, CenterX - 100, CenterY - 100, CenterX + 100, CenterY + 100);

	/* Draw the chopsticks */
	dDeltaAng = 360 / PHILOSOPHERS;    //筷子间的角度差
	for (pos = 0; pos < PHILOSOPHERS; pos++)	//FIXIT
	{
		/* Draw the chopsticks */
		AngRad = (pos * dDeltaAng)/57.29577951;  //转化为弧度
		dx = CenterX + (sin(AngRad)*60);
		dy = CenterY - (cos(AngRad)*60);
		MoveToEx(hdc, (int)dx, (int)dy, NULL);
		dx = CenterX + (sin(AngRad)*85);
		dy = CenterY - (cos(AngRad)*85);
		LineTo(hdc, (int)dx, (int)dy);

		//Draw the plate
		AngRad = ((pos * dDeltaAng+dDeltaAng / 2))/57.29577951;  //转化为弧度
		dx = CenterX + (sin(AngRad) * 72);
		dy = CenterY - (cos(AngRad) * 72);
		Ellipse(hdc, (int)dx-12, (int)dy-12, (int)dx+12, (int)dy+12);
	}

	/* delete the black pen */
	DeleteObject(SelectObject(hdc, hPen));

	/* Draw the philosophers */
	for(pos = 0; pos < PHILOSOPHERS; pos++)
	{
		/* select a pen for each philosopher */
		switch (gDinerState[pos])
		{
		case RESTING:
			hPen = SelectObject(hdc, CreatePen(PS_SOLID, 3, RGB(0, 255, 0)));
			break;

		case WAITING:
		case EATING:
			hPen = SelectObject(hdc, CreatePen(PS_SOLID, 3, RGB(255, 0, 0)));
			break;

		default:
			hPen = SelectObject(hdc, CreatePen(PS_SOLID, 3, 0L));
		}

		AngRad = ((pos * dDeltaAng) + dDeltaAng / 2)/57.29577951;
		px = CenterX + (sin(AngRad)*150);
		py = CenterY - (cos(AngRad)*150);

		/* Draw the Philosopher */
		Ellipse(hdc, (int)px-25, (int)py-25, (int)px+25, (int)py+25);

		//Draw the left arm
		if (gChopstickState[pos] == pos)
		{
			MoveToEx(hdc, (int)px, (int)py, NULL);
			AngRad = (pos * dDeltaAng)/57.29577951; //转化为弧度
			dx = CenterX + (sin(AngRad)*85);
			dy = CenterY - (cos(AngRad)*85);
			LineTo(hdc, (int)dx, (int)dy);
		}

		//Draw the right arm
		p1 = pos + 1;
		if (p1 == PHILOSOPHERS)
			p1 = 0;
		if (gChopstickState[p1] == pos)
		{
			MoveToEx(hdc, (int)px, (int)py, NULL);
			AngRad = (p1 * dDeltaAng)/57.29577951;
			dx = CenterX + (sin(AngRad)*85);
			dy = CenterY - (cos(AngRad)*85);
			LineTo(hdc, (int)dx, (int)dy);
		}

		/* Delete the pen */
		DeleteObject(SelectObject(hdc, hPen));			
	}	//for pos

	BitBlt( hDestDC,
				rect.left,
				rect.top,
				rect.right - rect.left,
				rect.bottom-rect.top,
				hdc,
				rect.left,
				rect.top,
				SRCCOPY
			);
	GetLastError();

	SelectObject(hdc, hOldBitmap);

//	DeleteDC(hWndMain, hdc);
}

/********************************************************************/
/*	ROUTINE:	InitApplication										*/
/*																	*/
/*	PURPOSE:	Initialize the application							*/
/********************************************************************/

BOOL InitApplication(HINSTANCE hInstance)
{
	WNDCLASS  wc;

	wc.style = CS_HREDRAW | CS_VREDRAW;
	wc.lpfnWndProc = WndProc;
	wc.cbClsExtra = 0;
	wc.cbWndExtra = 0;
	wc.hInstance = hInstance;
	wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1); 
	wc.lpszMenuName =  "din";
	wc.lpszClassName = "dinWClass";

	RegisterClass(&wc);

	return TRUE;
}


/********************************************************************/
/* ROUTINE:  InitInstance											*/
/*																	*/
/* PURPOSE:  Saves instance handle and creates main window			*/
/********************************************************************/

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	int ret;

	hInst = hInstance;

	hWndMain = CreateWindow(
		"dinWClass",
		"Dining Philosopher",
		WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT,
		CW_USEDEFAULT,
		450,
		450,
		NULL, NULL, hInstance, NULL );

	if (!hWndMain)
		return FALSE;

	ShowWindow(hWndMain, nCmdShow);
	UpdateWindow(hWndMain);

	if (!CreateOffscreen())
		PostQuitMessage(1);

	ret = MessageBox(hWndMain, "你期望使用防死锁运行模式吗?\n\n"
		"如果选择Yes, 程序将正常运行.\n"
		"如果选择 No, 程序会进入死锁.\n",
		"Wait Mode", MB_YESNO);
	if (ret == IDYES)
		bWaitMultiple = TRUE;
	else
	{
		bWaitMultiple = FALSE;

		ret = MessageBox(hWndMain, "你期望快速进入死锁吗?\n\n"
			"如果选择Yes, 将更快进入死锁.\n",
			"Wait Mode", MB_YESNO);
		if (ret == IDYES)
			bFastFood = TRUE;
		else
			bFastFood = FALSE;
	}

	// Start the threads
	Diner();

	return TRUE;
}

/********************************************************************/
/* FUNCTION: WinMain												*/
/*																	*/
/* PURPOSE: Calls initialization function, processes message loop	*/
/********************************************************************/

int PASCAL WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, 
	LPSTR lpCmdLine, int nCmdShow)
{
	MSG msg;
	int i;

	if (!hPrevInstance)
		if (!InitApplication(hInstance))
	   		return (FALSE);

	if (!InitInstance(hInstance, nCmdShow))
  		return (FALSE);

	while (GetMessage(&msg, NULL, 0, 0)) 
	{
		TranslateMessage(&msg);
	 	DispatchMessage(&msg); 
	}
	// Clear the table
	for (i = 0; i < PHILOSOPHERS; i++)
		CloseHandle(gchopStick[i]); //关闭互斥体句柄
  	return (msg.wParam);
}
